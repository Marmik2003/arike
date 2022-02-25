from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from arike.health_center.forms import PatientFamilyMemberForm, PatientForm, PatientDiseaseForm
from arike.health_center.mixins import NurseRequiredMixin, PrimaryNurseRequiredMixin, SecondaryNurseRequiredMixin
from arike.health_center.models import Patient, PatientDisease, PatientFamilyMember


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
        form.instance.ward = self.request.user.facility.ward
        return super().form_valid(form)


class PatientUpdateView(PrimaryNurseRequiredMixin, UpdateView):
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
            facilities = self.request.user.facility.phc_set.all() | self.request.user.facility
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
            facilities = self.request.user.facility.phc_set.all() | self.request.user.facility
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
            facilities = self.request.user.facility.phc_set.all() | self.request.user.facility
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
            facilities = self.request.user.facility.phc_set.all() | self.request.user.facility
            patient = Patient.objects.get(
                id=self.kwargs['patient_id'],
                facility__in=facilities,
            )
            return PatientDisease.objects.filter(patient=patient)

