from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from arike.health_center.forms import ProfileForm
from arike.health_center.mixins import NurseRequiredMixin
from arike.users.tasks import User


class HomeView(NurseRequiredMixin, TemplateView):
    template_name = 'health_center/home.html'


class ProfileView(NurseRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        form = ProfileForm(instance=user)
        return render(request, 'district_admin/profile.html', {'form': form})

    def post(self, request):
        user = User.objects.get(pk=request.user.id)
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('district_admin:home')
        return render(request, 'district_admin/profile.html', {'form': form})
