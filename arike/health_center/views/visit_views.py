from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, TemplateView, DetailView

from arike.district_admin.models import Facility
from arike.health_center.mixins import NurseRequiredMixin
from arike.health_center.forms import *
from arike.health_center.models import PatientVisitSchedule, PatientVisitDetail
from arike.users.tasks import send_relative_report


class ScheduledVisitListView(NurseRequiredMixin, TemplateView):
    model = PatientVisitSchedule
    template_name = 'health_center/visits/list_scheduled.html'

    def _filter_queryset(self, queryset: PatientVisitSchedule.objects):
        if 'facility' in self.request.GET:
            queryset = queryset.filter(
                patient__facility__name__icontains=self.request.GET['facility']
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'sec_nurse':
            context['facilities'] = self.request.user.facility.phc_set.all()
        if PatientVisitSchedule.objects.filter(
            nurse=self.request.user,
            date__gte=timezone.now(),
            visited=False
        ).count() == 0:
            context['no_visits'] = True
            context['today_visits'] = PatientVisitSchedule.objects.none()
            context['tomorrow_visits'] = PatientVisitSchedule.objects.none()
            context['future_visits'] = PatientVisitSchedule.objects.none()
        else:
            context['today_visits'] = self._filter_queryset(PatientVisitSchedule.objects.filter(
                nurse=self.request.user,
                date__gte=timezone.now().date(),
                date__lt=timezone.now().date() + timezone.timedelta(days=1),
                visited=False
            ))
            context['tomorrow_visits'] = self._filter_queryset(PatientVisitSchedule.objects.filter(
                nurse=self.request.user,
                date__gte=timezone.now().date() + timezone.timedelta(days=1),
                date__lt=timezone.now().date() + timezone.timedelta(days=2),
                visited=False
            ))
            context['future_visits'] = self._filter_queryset(PatientVisitSchedule.objects.filter(
                nurse=self.request.user,
                date__gte=timezone.now().date() + timezone.timedelta(days=2),
                visited=False
            ))

        return context


class ScheduleCreateView(NurseRequiredMixin, CreateView):
    model = PatientVisitSchedule
    form_class = PatientVisitScheduleForm
    template_name = 'health_center/visits/create_schedule.html'
    success_url = reverse_lazy('health_center:visit_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'sec_nurse':
            context['facilities'] = self.request.user.facility.phc_set.all()
        return context

    def form_valid(self, form):
        form.instance.nurse = self.request.user
        form.instance.patient = Patient.objects.get(id=self.kwargs['patient_id'])
        return super().form_valid(form)


class ScheduleDeleteView(NurseRequiredMixin, DeleteView):
    model = PatientVisitSchedule
    template_name = 'health_center/visits/delete_schedule.html'
    success_url = reverse_lazy('health_center:visit_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class VisitDetailsCreateView(NurseRequiredMixin, CreateView):
    model = PatientVisitDetail
    form_class = PatientVisitDetailForm
    template_name = 'health_center/visits/create_visit_details.html'
    success_url = reverse_lazy('health_center:visit_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule'] = PatientVisitSchedule.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        visit_schedule = PatientVisitSchedule.objects.get(id=self.kwargs['pk'])
        form.instance.patient_visit_schedule = visit_schedule
        visit_schedule.visited = True
        visit_schedule.save()
        visit = form.save()
        send_relative_report.delay(visit.id)
        return super().form_valid(form)


class VisitDetailView(NurseRequiredMixin, DetailView):
    model = PatientVisitDetail
    template_name = 'health_center/visits/visit_detail.html'

    def get_queryset(self):
        if self.request.user.role == 'sec_nurse':
            facilities = self.request.user.facility.phc_set.all()
            queryset = PatientVisitDetail.objects.filter(
                patient_visit_schedule__patient__facility__in=facilities,
            ) | PatientVisitDetail.objects.filter(
                patient_visit_schedule__patient__facility=self.request.user.facility,
            )
            return queryset
        else:
            return PatientVisitDetail.objects.filter(
                patient_visit_schedule__patient__facility=self.request.user.facility,
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule = PatientVisitSchedule.objects.get(id=self.kwargs['pk'])
        context['patient'] = schedule.patient
        return context
