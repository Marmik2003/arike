from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from arike.district_admin.models import Facility
from arike.health_center.mixins import NurseRequiredMixin
from arike.health_center.forms import PatientFamilyMemberForm, PatientForm, PatientDiseaseForm, PatientTreatmentForm, \
    TreatmentNoteForm
from arike.health_center.models import Patient, PatientFamilyMember, PatientDisease, PatientTreatment, TreatmentNote, \
    PatientVisitSchedule, PatientVisitDetail


# Patient Views
class PatientListView(NurseRequiredMixin, ListView):
    model = Patient
    template_name = 'health_center/patients/patient_list.html'

    def _filter_queryset(self, queryset):
        if self.request.GET.get('facility'):
            queryset = queryset.filter(facility__name__icontains=self.request.GET.get('facility'))
        if self.request.GET.get('query'):
            queryset = queryset.filter(
                full_name__icontains=self.request.GET.get('query'),
            ) | queryset.filter(
                phone__icontains=self.request.GET.get('query'),
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'sec_nurse':
            context['facilities'] = self.request.user.facility.phc_set.all()

        return context

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            queryset = Patient.objects.filter(
                facility=self.request.user.facility,
            )
        elif self.request.user.role == 'sec_nurse':
            facility = self.request.user.facility
            phc_set = facility.phc_set.all()
            patients = Patient.objects.filter(
                facility__in=phc_set,
            ) | Patient.objects.filter(
                facility=facility,
            )
            queryset = patients
        else:
            queryset = Patient.objects.none()
        return self._filter_queryset(queryset)


class PatientCreateView(NurseRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy('health_center:patient_list')
    template_name = 'health_center/patients/create_patient.html'

    def form_valid(self, form):
        form.instance.facility = self.request.user.facility
        form.instance.nurse = self.request.user
        form.instance.ward = self.request.user.facility.ward
        return super().form_valid(form)


class PatientUpdateView(NurseRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy('health_center:patient_list')
    template_name = 'health_center/patients/edit_patient.html'

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            return Patient.objects.filter(
                facility=self.request.user.facility,
            )
        elif self.request.user.role == 'sec_nurse':
            facility = self.request.user.facility
            phc_set = facility.phc_set.all()
            patients = Patient.objects.filter(
                facility__in=phc_set,
            ) | Patient.objects.filter(
                facility=facility,
            )
            return patients
        else:
            return Patient.objects.none()


class PatientDeleteView(NurseRequiredMixin, DeleteView):
    model = Patient
    success_url = reverse_lazy('health_center:patient_list')
    template_name = 'health_center/patients/delete_patient.html'

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            return Patient.objects.filter(
                facility=self.request.user.facility,
            )
        elif self.request.user.role == 'sec_nurse':
            facility = self.request.user.facility
            phc_set = facility.phc_set.all()
            patients = Patient.objects.filter(
                facility__in=phc_set,
            ) | Patient.objects.filter(
                facility=facility,
            )
            return patients
        else:
            return Patient.objects.none()

    def delete(self, request, *args, **kwargs):
        patient = self.get_object()
        patient.deleted = True
        patient.save()
        return HttpResponseRedirect(self.success_url)


class PatientDetailView(NurseRequiredMixin, DetailView):
    model = Patient
    template_name = 'health_center/patients/patient_detail.html'

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            return Patient.objects.filter(
                facility=self.request.user.facility,
            )
        elif self.request.user.role == 'sec_nurse':
            facility = self.request.user.facility
            phc_set = facility.phc_set.all()
            patients = Patient.objects.filter(
                facility__in=phc_set,
            ) | Patient.objects.filter(
                facility=facility,
            )
            return patients
        else:
            return Patient.objects.none()


# Patient Family Views
class PatientFamilyListView(NurseRequiredMixin, ListView):
    model = PatientFamilyMember
    template_name = 'health_center/patients/list_family_members.html'

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility=self.request.user.facility,
            )
            return PatientFamilyMember.objects.filter(
                patient=patient,
            )
        elif self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()\
                         | Facility.objects.filter(id=self.request.user.facility.id)
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility__in=facilities,
            )
            return PatientFamilyMember.objects.filter(patient=patient)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs['patient_id'])
        return context


class PatientFamilyCreateView(NurseRequiredMixin, CreateView):
    model = PatientFamilyMember
    form_class = PatientFamilyMemberForm
    template_name = 'health_center/patients/create_family_member.html'

    def form_valid(self, form):
        patient = Patient.objects.get(
            id=self.kwargs['patient_id'],
            facility=self.request.user.facility,
        )
        form.instance.patient = patient
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('health_center:patient_detail', kwargs={'pk': self.kwargs['patient_id']})


class PatientFamilyUpdateView(NurseRequiredMixin, UpdateView):
    model = PatientFamilyMember
    form_class = PatientFamilyMemberForm
    template_name = 'health_center/patients/edit_family_member.html'

    def get_success_url(self):
        return reverse_lazy('health_center:patient_detail', kwargs={'pk': self.kwargs['patient_id']})


class PatientFamilyDeleteView(NurseRequiredMixin, DeleteView):
    model = PatientFamilyMember
    success_url = reverse_lazy('health_center:patient_list')
    template_name = 'health_center/patients/delete_family_member.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs['patient_id'])
        return context

    def delete(self, request, *args, **kwargs):
        patient_family_member = self.get_object()
        patient_family_member.deleted = True
        patient_family_member.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('health_center:patient_detail', kwargs={'pk': self.kwargs['patient_id']})


# Patient Disease Views
class PatientDiseaseListView(NurseRequiredMixin, ListView):
    model = PatientDisease
    template_name = 'health_center/patients/disease_list.html'

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility=self.request.user.facility,
            )
            return PatientDisease.objects.filter(
                patient=patient,
            )
        elif self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()\
                         | Facility.objects.filter(id=self.request.user.facility.id)
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility__in=facilities,
            )
            return PatientDisease.objects.filter(patient=patient)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs['patient_id'])
        return context


class PatientDiseaseCreateView(NurseRequiredMixin, CreateView):
    model = PatientDisease
    form_class = PatientDiseaseForm
    template_name = 'health_center/patients/create_disease.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs['patient_id'])
        return context

    def form_valid(self, form):
        patient = Patient.objects.get(
            id=self.kwargs['patient_id'],
            facility=self.request.user.facility,
        )
        form.instance.patient = patient
        form.instance.investigated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('health_center:patient_detail', kwargs={'pk': self.kwargs['patient_id']})


class PatientDiseaseUpdateView(NurseRequiredMixin, UpdateView):
    model = PatientDisease
    form_class = PatientDiseaseForm
    template_name = 'health_center/patients/edit_disease.html'

    def get_success_url(self):
        return reverse_lazy('health_center:patient_detail', kwargs={'pk': self.kwargs['patient_id']})

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility=self.request.user.facility,
            )
            return PatientDisease.objects.filter(
                patient=patient,
            )
        elif self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()\
                         | Facility.objects.filter(id=self.request.user.facility.id)
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility__in=facilities,
            )
            return PatientDisease.objects.filter(patient=patient)


class PatientDiseaseDeleteView(NurseRequiredMixin, DeleteView):
    model = PatientDisease
    success_url = reverse_lazy('health_center:patient_list')
    template_name = 'health_center/patients/delete_disease.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs['patient_id'])
        return context

    def delete(self, request, *args, **kwargs):
        patient_disease = self.get_object()
        patient_disease.deleted = True
        patient_disease.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('health_center:patient_detail', kwargs={'pk': self.kwargs['patient_id']})

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility=self.request.user.facility,
            )
            return PatientDisease.objects.filter(
                patient=patient,
            )
        elif self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()\
                         | Facility.objects.filter(id=self.request.user.facility.id)
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility__in=facilities,
            )
            return PatientDisease.objects.filter(patient=patient)


# Patient Treatment Views
class PatientTreatmentListView(NurseRequiredMixin, ListView):
    model = PatientTreatment
    template_name = 'health_center/patients/treatment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs['patient_id'])
        return context

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility=self.request.user.facility,
            )
            return PatientTreatment.objects.filter(
                patient=patient,
            )
        elif self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()\
                         | Facility.objects.filter(id=self.request.user.facility.id)
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility__in=facilities,
            )
            return PatientTreatment.objects.filter(patient=patient)


class PatientTreatmentCreateView(NurseRequiredMixin, CreateView):
    model = PatientTreatment
    form_class = PatientTreatmentForm
    template_name = 'health_center/patients/add_treatment.html'

    def get_success_url(self):
        return reverse_lazy('health_center:patient_detail', kwargs={'pk': self.kwargs['patient_id']})

    def form_valid(self, form):
        patient = Patient.objects.get(id=self.kwargs['patient_id'])
        form.instance.patient = patient
        form.instance.given_by = self.request.user
        form.instance.is_active = True
        return super().form_valid(form)


class PatientTreatmentUpdateView(NurseRequiredMixin, UpdateView):
    model = PatientTreatment
    form_class = PatientTreatmentForm
    template_name = 'health_center/patients/update_treatment.html'

    def get_success_url(self):
        return reverse_lazy('health_center:patient_detail', kwargs={'pk': self.kwargs['patient_id']})

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility=self.request.user.facility,
            )
            return PatientTreatment.objects.filter(
                patient=patient,
            )
        elif self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()\
                         | Facility.objects.filter(id=self.request.user.facility.id)
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility__in=facilities,
            )
            return PatientTreatment.objects.filter(patient=patient)


class PatientTreatmentDeleteView(NurseRequiredMixin, DeleteView):
    model = PatientTreatment
    template_name = 'health_center/patients/delete_treatment.html'

    def get_success_url(self):
        return reverse_lazy('health_center:patient_detail', kwargs={'pk': self.kwargs['patient_id']})

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility=self.request.user.facility,
            )
            return PatientTreatment.objects.filter(
                patient=patient,
            )
        elif self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()\
                         | Facility.objects.filter(id=self.request.user.facility.id)
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility__in=facilities,
            )
            return PatientTreatment.objects.filter(patient=patient)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs['patient_id'])
        return context


class PatientTreatmentDetailView(NurseRequiredMixin, DetailView):
    model = PatientTreatment
    template_name = 'health_center/patients/detail_treatment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs['patient_id'])
        treatment = PatientTreatment.objects.get(id=self.kwargs['pk'])
        context['treatment_notes'] = TreatmentNote.objects.filter(patient_treatment=treatment)
        return context

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility=self.request.user.facility,
            )
            return PatientTreatment.objects.filter(
                patient=patient,
            )
        elif self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()\
                         | Facility.objects.filter(id=self.request.user.facility.id)
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility__in=facilities,
            )
            return PatientTreatment.objects.filter(patient=patient)


class PatientTreatmentNoteCreateView(NurseRequiredMixin, CreateView):
    model = TreatmentNote
    form_class = TreatmentNoteForm
    template_name = 'health_center/patients/create_treatment_note.html'

    def get_success_url(self):
        return reverse_lazy('health_center:patient_treatment_detail', kwargs={
            'patient_id': self.kwargs['patient_id'],
            'pk': self.kwargs['treatment_id'],
        })

    def form_valid(self, form):
        treatment = PatientTreatment.objects.get(id=self.kwargs['treatment_id'])
        form.instance.patient_treatment = treatment
        form.instance.nurse = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['treatment'] = PatientTreatment.objects.get(id=self.kwargs['treatment_id'])
        return context


class PatientTreatmentNoteUpdateView(NurseRequiredMixin, UpdateView):
    model = TreatmentNote
    form_class = TreatmentNoteForm
    template_name = 'health_center/patients/update_treatment_note.html'

    def get_success_url(self):
        return reverse_lazy('health_center:patient_treatment_detail', kwargs={
            'patient_id': self.kwargs['patient_id'],
            'pk': self.kwargs['treatment_id'],
        })

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility=self.request.user.facility,
            )
            queryset = PatientTreatment.objects.filter(
                patient=patient,
            )
        elif self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()\
                         | Facility.objects.filter(id=self.request.user.facility.id)
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility__in=facilities,
            )
            queryset = PatientTreatment.objects.filter(patient=patient, given_by=self.request.user)
        return TreatmentNote.objects.filter(patient_treatment__in=queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['treatment'] = PatientTreatment.objects.get(id=self.kwargs['treatment_id'])
        return context


class PatientTreatmentNoteDeleteView(NurseRequiredMixin, DeleteView):
    model = TreatmentNote
    template_name = 'health_center/patients/delete_treatment_note.html'

    def get_success_url(self):
        return reverse_lazy('health_center:patient_treatment_detail', kwargs={
            'patient_id': self.kwargs['patient_id'],
            'pk': self.kwargs['treatment_id'],
        })

    def get_queryset(self):
        if self.request.user.role == 'pri_nurse':
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility=self.request.user.facility,
            )
            queryset = PatientTreatment.objects.filter(
                patient=patient,
            )
        elif self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()\
                         | Facility.objects.filter(id=self.request.user.facility.id)
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility__in=facilities,
            )
            queryset = PatientTreatment.objects.filter(patient=patient, given_by=self.request.user)
        else:
            queryset = PatientTreatment.objects.none()

        return TreatmentNote.objects.filter(patient_treatment__in=queryset)


# Patient Visit Views
class PatientVisitListView(NurseRequiredMixin, ListView):
    model = PatientVisitSchedule
    template_name = 'health_center/patients/patient_visit_history.html'

    def get_queryset(self):
        schedules = PatientVisitSchedule.objects.filter(
            patient=Patient.objects.get(id=self.kwargs['patient_id']),
            visited=True,
        )
        if self.request.user.role == 'pri_nurse':
            return  schedules.filter(
                patient__facility=self.request.user.facility,
            )
        elif self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()\
                                     | Facility.objects.filter(id=self.request.user.facility.id)
            return schedules.filter(
                patient__facility__in=facilities,
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs['patient_id'])
        return context
