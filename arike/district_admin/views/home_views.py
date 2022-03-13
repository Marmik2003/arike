from django.contrib import messages
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
            password_change = False
            if form.cleaned_data.get('new_password'):
                password_change = True
            form.save()
            if password_change:
                messages.success(request, 'Password changed successfully, please login again')
            return redirect('district_admin:home')
        return render(request, 'district_admin/profile.html', {'form': form})

