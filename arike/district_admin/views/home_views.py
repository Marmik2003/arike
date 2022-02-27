from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, UpdateView

from arike.district_admin.forms import ProfileForm
from arike.district_admin.mixins import DistrictAdminRequiredMixin
from arike.users.tasks import User


class HomeView(DistrictAdminRequiredMixin, TemplateView):
    template_name = 'district_admin/home.html'


class ProfileView(DistrictAdminRequiredMixin, View):
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

