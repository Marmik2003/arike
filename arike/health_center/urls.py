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
    PatientTreatmentListView,
    PatientTreatmentCreateView,
    PatientTreatmentUpdateView,
    PatientTreatmentDeleteView,
    PatientTreatmentDetailView,
    PatientTreatmentNoteCreateView,
    PatientTreatmentNoteUpdateView,
    PatientTreatmentNoteDeleteView,
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

# Patient Treatment Views
urlpatterns += [
    path(
        'patients/<int:patient_id>/treatments/',
        PatientTreatmentListView.as_view(),
        name='patient_treatment_list'
    ),
    path(
        'patients/<int:patient_id>/treatments/create/',
        PatientTreatmentCreateView.as_view(),
        name='patient_treatment_create'
    ),
    path(
        'patients/<int:patient_id>/treatments/<int:pk>/update/',
        PatientTreatmentUpdateView.as_view(),
        name='patient_treatment_update'
    ),
    path(
        'patients/<int:patient_id>/treatments/<int:pk>/delete/',
        PatientTreatmentDeleteView.as_view(),
        name='patient_treatment_delete'
    ),
    path(
        'patients/<int:patient_id>/treatments/<int:pk>/',
        PatientTreatmentDetailView.as_view(),
        name='patient_treatment_detail'
    ),
]

# Patient Treatment Note Views
urlpatterns += [
    path(
        'patients/<int:patient_id>/treatments/<int:treatment_id>/notes/create/',
        PatientTreatmentNoteCreateView.as_view(),
        name='patient_treatment_note_create'
    ),
    path(
        'patients/<int:patient_id>/treatments/<int:treatment_id>/notes/<int:pk>/update/',
        PatientTreatmentNoteUpdateView.as_view(),
        name='patient_treatment_note_update'
    ),
    path(
        'patients/<int:patient_id>/treatments/<int:treatment_id>/notes/<int:pk>/delete/',
        PatientTreatmentNoteDeleteView.as_view(),
        name='patient_treatment_note_delete'
    ),
]
