from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from arike.users.forms import UserLoginForm
from arike.users.views import RedirectView, ChangePasswordView

app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html', authentication_form=UserLoginForm),
         name='login'),
    path('redirect/', RedirectView.as_view(), name='redirect'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
