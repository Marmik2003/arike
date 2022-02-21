from django.urls import path
from arike.district_admin.views.home_views import HomeView

app_name = 'district_admin'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
