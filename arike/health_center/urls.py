from django.urls import path

from arike.health_center.views.common_views import HomeView
from arike.health_center.views.patient_views import (
    PatientListView,
    PatientCreateView,
    PatientUpdateView,
    PatientDeleteView,
    PatientDetailView,
    PatientFamilyListView,
    PatientFamilyCreateView,
    PatientFamilyUpdateView,
    PatientFamilyDeleteView,
    PatientDiseaseListView,
    PatientDiseaseCreateView,
    PatientDiseaseUpdateView,
    PatientDiseaseDeleteView,
)

app_name = 'health_center'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]

# Patient Views
urlpatterns += [
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('patients/create/', PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/update/', PatientUpdateView.as_view(), name='patient_update'),
    path('patients/<int:pk>/delete/', PatientDeleteView.as_view(), name='patient_delete'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
]

# Patient Family Views
urlpatterns += [
    path(
        'patients/<int:patient_id>/families/',
        PatientFamilyListView.as_view(),
        name='patient_family_list'
    ),
    path(
        'patients/<int:patient_id>/families/create/',
        PatientFamilyCreateView.as_view(),
        name='patient_family_create'
    ),
    path(
        'patients/<int:patient_id>/families/<int:pk>/update/',
        PatientFamilyUpdateView.as_view(),
        name='patient_family_update'
    ),
    path(
        'patients/<int:patient_id>/families/<int:pk>/delete/',
        PatientFamilyDeleteView.as_view(),
        name='patient_family_delete'
    ),
]

# Patient Disease Views
urlpatterns += [
    path(
        'patients/<int:patient_id>/diseases/',
        PatientDiseaseListView.as_view(),
        name='patient_disease_list'
    ),
    path(
        'patients/<int:patient_id>/diseases/create/',
        PatientDiseaseCreateView.as_view(),
        name='patient_disease_create'
    ),
    path(
        'patients/<int:patient_id>/diseases/<int:pk>/update/',
        PatientDiseaseUpdateView.as_view(),
        name='patient_disease_update'
    ),
    path(
        'patients/<int:patient_id>/diseases/<int:pk>/delete/',
        PatientDiseaseDeleteView.as_view(),
        name='patient_disease_delete'
    ),
]
