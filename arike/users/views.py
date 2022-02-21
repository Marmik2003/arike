from django.shortcuts import redirect
from django.views import View


class RedirectView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admin:index')
            elif request.user.role == 'dist_admin':
                return redirect('district_admin:home')
            elif request.user.role == 'sec_nurse':
                pass
            elif request.user.role == 'pri_nurse':
                pass
            else:
                pass
        return redirect('users:login')
