from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from arike.district_admin.mixins import DistrictAdminRequiredMixin
from arike.district_admin.models import Ward, Facility, FACILITY_KIND
from arike.users.models import User, USER_ROLES
from arike.district_admin.forms import UserForm
from arike.users.tasks import new_user_onboarding


class AllUsersView(DistrictAdminRequiredMixin, ListView):
    model = User
    template_name = 'district_admin/users/list.html'
    context_object_name = 'users'
    paginate_by = 10

    def _filter_queryset(self, queryset: User.objects):
        ward = self.request.GET.get('ward')
        if ward:
            queryset = queryset.filter(facility__ward__name=ward)
        if self.request.GET.get('facility'):
            pass

        if self.request.GET.get('role'):
            queryset = queryset.filter(role=self.request.GET.get('role'))

        if self.request.GET.get('query'):
            queryset = queryset.filter(
                first_name__icontains=self.request.GET.get('query'),
            ) | queryset.filter(
                last_name__icontains=self.request.GET.get('query'),
            ) | queryset.filter(
                phone_number__icontains=self.request.GET.get('query'),
            )

        return queryset.filter(is_active=True)

    def get_queryset(self):
        queryset = User.objects.filter(district=self.request.user.district).exclude(role=USER_ROLES[0][0])
        return self._filter_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wards'] = Ward.objects.filter(localbody__district=self.request.user.district)
        context['user_roles'] = USER_ROLES[1:]
        return context


class CreateUserView(DistrictAdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'district_admin/users/create.html'
    success_url = reverse_lazy('district_admin:users')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form['facility'].queryset = Facility.objects.filter(
            ward__localbody__district=self.request.user.district
        )
        return form

    def form_valid(self, form):
        form.instance.district = self.request.user.district
        form.instance.password = make_password('Arike@101#')
        form = form.save()
        new_user_onboarding.delay(form.id)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wards'] = Ward.objects.filter(localbody__district=self.request.user.district)

        return context


class UpdateUserView(DistrictAdminRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'district_admin/users/update.html'
    success_url = reverse_lazy('district_admin:users')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        current_ward = self.object.facility.ward
        form['facility'].queryset = Facility.objects.filter(
            ward__localbody__district=self.request.user.district,
            ward=current_ward
        )
        return form

    def get_queryset(self):
        return User.objects.filter(district=self.request.user.district)

    def form_valid(self, form):
        form.instance.district = self.request.user.district

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wards'] = Ward.objects.filter(localbody__district=self.request.user.district)
        context['current_ward'] = self.object.facility.ward
        return context


class DeleteUserView(DistrictAdminRequiredMixin, DeleteView):
    model = User
    template_name = 'district_admin/users/delete.html'
    success_url = reverse_lazy('district_admin:users')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return HttpResponseRedirect(self.success_url)

    def get_queryset(self):
        return User.objects.filter(district=self.request.user.district)


class DetailUserView(DistrictAdminRequiredMixin, DetailView):
    model = User
    template_name = 'district_admin/users/detail.html'
    context_object_name = 'user'

    def get_queryset(self):
        return User.objects.filter(district=self.request.user.district)


def get_facility_from_ward(request):
    if request.user.is_authenticated:
        ward_id = request.GET.get('ward')

        if 'get_id' in request.GET:
            facilities = Facility.objects.filter(
                ward_id=ward_id,
                ward__localbody__district=request.user.district
            )
            return HttpResponse(
                '<option value="">Select Facility</option>' +
                ''.join(['<option value="{}">{}</option>'.format(f.id, f.name) for f in facilities])
            )
        elif 'get_chc' in request.GET:
            facilities = Facility.objects.filter(
                ward_id=ward_id,
                ward__localbody__district=request.user.district,
                kind=FACILITY_KIND[1][0]
            )
            return HttpResponse(
                '<option value="">Select CHC</option>' +
                ''.join(['<option value="{}">{}</option>'.format(f.id, f.name) for f in facilities])
            )
        else:
            facilities = Facility.objects.filter(
                ward__name=ward_id,
                ward__localbody__district=request.user.district
            )
            return HttpResponse(
                '<option value="">Select Facility</option>' +
                ''.join(['<option value="{}">{}</option>'.format(f.name, f.name) for f in facilities])
            )
    else:
        return HttpResponse('District Admin Only')


def is_facility_chc(request):
    if request.user.is_authenticated and request.user.role == USER_ROLES[0][0]:
        facility_id = request.GET.get('facility')
        facility = Facility.objects.get(id=facility_id)
        if facility.kind == FACILITY_KIND[1][0]:
            return HttpResponse('true')
        else:
            return HttpResponse('false')
