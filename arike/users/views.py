from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import View

from arike.users.forms import PasswordChangeForm


class RedirectView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if not request.user.is_verified:
                return redirect('users:change_password')
            if request.user.is_superuser:
                return redirect('admin:index')
            elif request.user.role == 'dist_admin':
                return redirect('district_admin:home')
            elif request.user.role == 'sec_nurse':
                return redirect('health_center:home')
            elif request.user.role == 'pri_nurse':
                return redirect('health_center:home')
            else:
                pass
        return redirect('users:login')


class ChangePasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = PasswordChangeForm()
            return render(request, 'users/password_change.html', context={'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                if password1 == password2:
                    request.user.set_password(password1)
                    request.user.is_verified = True
                    request.user.save()
                    messages.success(request, 'Password changed successfully')
                    return redirect('users:login')
                else:
                    messages.error(request, 'Passwords do not match')
                    return redirect('users:change_password')
            else:
                return render(request, 'users/password_change.html', context={'form': form})
        else:
            return redirect('users:login')
