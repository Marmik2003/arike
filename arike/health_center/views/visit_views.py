from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from arike.district_admin.models import Facility
from arike.health_center.mixins import NurseRequiredMixin
from arike.health_center.forms import *
from arike.health_center.models import Patient, PatientDisease, PatientTreatment,PatientVisitSchedule, PatientVisitDetail


class ScheduledVisitListView(NurseRequiredMixin, ListView):
    model = PatientVisitSchedule
    template_name = 'health_center/visits/list_scheduled.html'

    def get_queryset(self):
        return PatientVisitSchedule.objects.filter(
            nurse=self.request.user,
            date__gte=timezone.now()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'sec_nurse':
            context['facilities'] = self.request.user.facility.phc_set.all()
        return context


class ScheduleCreateView(NurseRequiredMixin, CreateView):
    model = PatientVisitSchedule
    form_class = PatientVisitScheduleForm
    template_name = 'health_center/visits/create_schedule.html'
    success_url = reverse_lazy('health_center:visits:list_scheduled')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'sec_nurse':
            context['facilities'] = self.request.user.facility.phc_set.all()
        return context

    def form_valid(self, form):
        form.instance.nurse = self.request.user
        return super().form_valid(form)


class ScheduleDeleteView(NurseRequiredMixin, DeleteView):
    model = PatientVisitSchedule
    template_name = 'health_center/visits/delete_schedule.html'
    success_url = reverse_lazy('health_center:visits:list_scheduled')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class VisitDetailsCreateView(NurseRequiredMixin, CreateView):
    model = PatientVisitDetail
    form_class = PatientVisitDetailForm
    template_name = 'health_center/visits/create_visit_details.html'
    success_url = reverse_lazy('health_center:visits:list_scheduled')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule'] = PatientVisitSchedule.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.schedule = PatientVisitSchedule.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)
