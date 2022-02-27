from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from arike.health_center.forms import ProfileForm
from arike.health_center.mixins import NurseRequiredMixin
from arike.users.models import NurseReportSetting
from arike.users.tasks import User


class HomeView(NurseRequiredMixin, TemplateView):
    template_name = 'health_center/home.html'


class ProfileView(NurseRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        report = NurseReportSetting.objects.filter(nurse=user)
        if report.exists():
            report = report.first()
            enable_email_report = report.is_report_enabled
            report_time = report.report_time
            form = ProfileForm(
                instance=user,
                initial={
                    'enable_email_report': enable_email_report,
                    'report_time': report_time
                }
            )
        else:
            form = ProfileForm(instance=user)
        return render(request, 'health_center/profile.html', {'form': form})

    def post(self, request):
        user = User.objects.get(pk=request.user.id)
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('health_center:home')
        return render(request, 'health_center/profile.html', {'form': form})
