from django.urls import path
from arike.district_admin.views.home_views import HomeView, ProfileView
from arike.district_admin.views.facilities_views import (
    AllFacilitiesView,
    CreateFacilityView,
    UpdateFacilityView,
    DeleteFacilityView,
)
from arike.district_admin.views.users_views import (
    AllUsersView,
    CreateUserView,
    UpdateUserView,
    DeleteUserView,
    DetailUserView,
    get_facility_from_ward,
    is_facility_chc
)

app_name = 'district_admin'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

# Facilities
urlpatterns += [
    path('facilities/', AllFacilitiesView.as_view(), name='facilities'),
    path('facilities/create/', CreateFacilityView.as_view(), name='create_facility'),
    path('facilities/update/<int:pk>/', UpdateFacilityView.as_view(), name='update_facility'),
    path('facilities/delete/<int:pk>/', DeleteFacilityView.as_view(), name='delete_facility'),
]

# Users
urlpatterns += [
    path('users/', AllUsersView.as_view(), name='users'),
    path('users/create/', CreateUserView.as_view(), name='create_user'),
    path('users/update/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
    path('users/delete/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    path('users/detail/<int:pk>/', DetailUserView.as_view(), name='detail_user'),
]


# Ajax Paths
urlpatterns += [
    path('users/get_facility_from_ward/', get_facility_from_ward, name='get_facility_from_ward'),
    path('users/is_facility_chc/', is_facility_chc, name='is_facility_chc'),
]
