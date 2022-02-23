from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from arike.district_admin.mixins import DistrictAdminRequiredMixin
from arike.district_admin.models import Ward, Facility
from arike.users.models import User
from arike.district_admin.forms import UserForm


class AllUsersView(DistrictAdminRequiredMixin, ListView):
    model = User
    template_name = 'district_admin/users/list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(district=self.request.user.district)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wards'] = Ward.objects.filter(localbody__district=self.request.user.district)

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
        form.instance.password = 'Arike@101#'
        return super().form_valid(form)


class UpdateUserView(DistrictAdminRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'district_admin/users/update.html'
    success_url = reverse_lazy('district_admin:users')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form['facility'].queryset = Facility.objects.filter(
            ward__localbody__district=self.request.user.district
        )
        return form

    def form_valid(self, form):
        form.instance.district = self.request.user.district
        return super().form_valid(form)


class DeleteUserView(DistrictAdminRequiredMixin, DeleteView):
    model = User
    template_name = 'district_admin/users/delete.html'
    success_url = reverse_lazy('district_admin:users')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return HttpResponseRedirect(self.success_url)


class DetailUserView(DistrictAdminRequiredMixin, DetailView):
    model = User
    template_name = 'district_admin/users/detail.html'
    context_object_name = 'user'

    def get_queryset(self):
        return User.objects.filter(district=self.request.user.district)
