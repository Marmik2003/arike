from django.views.generic import ListView, CreateView, UpdateView

from arike.district_admin.forms import FacilityForm
from arike.district_admin.mixins import DistrictAdminRequiredMixin
from arike.district_admin.models import Facility


class AllFacilitiesView(DistrictAdminRequiredMixin, ListView):
    template_name = 'district_admin/facilities.html'
    context_object_name = 'facilities'
    model = Facility
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(ward__localbody__district=self.request.user.district)


class CreateFacilityView(DistrictAdminRequiredMixin, CreateView):
    template_name = 'district_admin/create_facility.html'
    model = Facility
    form_class = FacilityForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['ward'].queryset = form.fields['ward'].queryset.filter(
            localbody__district=self.request.user.district
        )
        return form

    def form_valid(self, form):
        form.instance.district = self.request.user.district
        return super().form_valid(form)


class EditFacilityView(DistrictAdminRequiredMixin, UpdateView):
    template_name = 'district_admin/edit_facility.html'
    model = Facility
    form_class = FacilityForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['ward'].queryset = form.fields['ward'].queryset.filter(
            localbody__district=self.request.user.district
        )
        return form

    def form_valid(self, form):
        form.instance.district = self.request.user.district
        return super().form_valid(form)
