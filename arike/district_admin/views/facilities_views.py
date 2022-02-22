from django.views.generic import ListView

from arike.district_admin.mixins import DistrictAdminRequiredMixin
from arike.district_admin.models import Facility


class AllFacilitiesView(DistrictAdminRequiredMixin, ListView):
    template_name = 'district_admin/facilities.html'
    context_object_name = 'facilities'
    model = Facility
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(district=self.request.user.district)
