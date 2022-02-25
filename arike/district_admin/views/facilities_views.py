from typing import Any, Dict

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from arike.district_admin.forms import FacilityForm
from arike.district_admin.mixins import DistrictAdminRequiredMixin
from arike.district_admin.models import Facility, Ward


class AllFacilitiesView(DistrictAdminRequiredMixin, ListView):
    template_name = 'district_admin/facilities/facilities.html'
    context_object_name = 'facilities'
    model = Facility
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['wards'] = Ward.objects.filter(localbody__district=self.request.user.district)
        return context

    def _filter_queryset(self, queryset: Facility.objects) -> Facility.objects:
        if 'ward' in self.request.GET:
            queryset = queryset.filter(ward__name__icontains=self.request.GET['ward'])
        if 'kind' in self.request.GET and self.request.GET['kind'] != '':
            queryset = queryset.filter(kind=self.request.GET['kind'])
        if 'query' in self.request.GET:
            queryset = queryset.filter(name__icontains=self.request.GET['query'])

        return queryset

    def get_queryset(self):
        queryset = self.model.objects.filter(ward__localbody__district=self.request.user.district)
        queryset = self._filter_queryset(queryset)
        return queryset


class CreateFacilityView(DistrictAdminRequiredMixin, CreateView):
    model = Facility
    form_class = FacilityForm
    template_name = 'district_admin/facilities/create_facility.html'
    success_url = reverse_lazy('district_admin:facilities')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['chc'].queryset = Facility.objects.filter(
            ward__localbody__district=self.request.user.district, kind='chc')
        form.fields['ward'].queryset = form.fields['ward'].queryset.filter(
            localbody__district=self.request.user.district
        )
        return form

    def form_valid(self, form):
        form.instance.district = self.request.user.district
        return super().form_valid(form)


class UpdateFacilityView(DistrictAdminRequiredMixin, UpdateView):
    template_name = 'district_admin/facilities/update_facility.html'
    model = Facility
    form_class = FacilityForm
    success_url = reverse_lazy('district_admin:facilities')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['chc'].queryset = Facility.objects.filter(
            ward__localbody__district=self.request.user.district, kind='chc')
        form.fields['ward'].queryset = form.fields['ward'].queryset.filter(
            localbody__district=self.request.user.district
        )
        return form

    def form_valid(self, form):
        form.instance.district = self.request.user.district
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_kind'] = self.get_object().kind
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(ward__localbody__district=self.request.user.district)
        return queryset


class DeleteFacilityView(DistrictAdminRequiredMixin, DeleteView):
    template_name = 'district_admin/facilities/delete_facility.html'
    model = Facility
    context_object_name = 'facility'
    success_url = reverse_lazy('district_admin:facilities')

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        facility = self.get_object()
        facility.deleted = True
        facility.save()
        return HttpResponseRedirect(self.success_url)

    def get_queryset(self):
        queryset = self.model.objects.filter(ward__localbody__district=self.request.user.district)
