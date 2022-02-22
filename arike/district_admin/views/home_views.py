from django.views.generic import TemplateView

from arike.district_admin.mixins import DistrictAdminRequiredMixin


class HomeView(DistrictAdminRequiredMixin, TemplateView):
    template_name = 'district_admin/home.html'

