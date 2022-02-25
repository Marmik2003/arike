from django.views.generic import TemplateView

from arike.health_center.mixins import NurseRequiredMixin


class HomeView(NurseRequiredMixin, TemplateView):
    template_name = 'health_center/home.html'
