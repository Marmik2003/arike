import logging
from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

from arike.health_center.models import Patient, PatientTreatment, TreatmentNote, PatientDisease, PatientVisitSchedule, \
    PatientVisitDetail
from arike.users.models import NurseReportSetting
from config import celery_app

logger = logging.getLogger(__name__)
User = get_user_model()

today = timezone.now()
yesterday = today - timedelta(days=1)


@celery_app.task()
def send_daily_report():
    """Celery task that sends daily report to nurse."""
    with transaction.atomic():
        reports = NurseReportSetting.objects.select_for_update().filter(last_sent_report_time__lte=yesterday)
        logger.info(f"reports {reports.count()}")
        for report in reports:
            user = User.objects.get(id=report.nurse.id)
            patients_count = Patient.objects.filter(nurse=user, created_date__gte=yesterday).count()
            yesterday_visits = PatientVisitSchedule.objects.filter(
                patient__nurse=user,
                date__gte=yesterday,
                date__lt=today
            ).count()
            patients_treated_count = PatientTreatment.objects.filter(given_by=user, created_date__gte=yesterday).count()
            patients_disease_count = PatientDisease.objects.filter(investigated_by=user, created_date__gte=yesterday)\
                .count()
            patients_notes_count = TreatmentNote.objects.filter(nurse=user, created_date__gte=yesterday).count()
            patients_treated_count += patients_notes_count
            today_visits = PatientVisitSchedule.objects.filter(
                date__gte=today,
                date__lte=today + timedelta(days=1),
                nurse=user
            ).count()
            context = {
                'user': user,
                'yesterday_visits': yesterday_visits,
                'yesterday_treatments': patients_treated_count,
                'yesterday_diseases': patients_disease_count,
                'yesterday_patients': patients_count,
                'today_visits': today_visits,
            }
            send_mail(
                "Daily Report",
                render_to_string('email_templates/daily_report.html', context),
                "marmik@thedataboy.com",
                [user.email, "marmik@thedataboy.com"],
            )
            report.last_sent_report_time = today
            report.save()
            logger.info(f"Daily report sent to {user.email}")


@celery_app.task()
def send_relative_report(visit_id):
    """Celery task that sends relative report to nurse."""
    with transaction.atomic():
        visit = PatientVisitDetail.objects.get(id=visit_id)
        patient = visit.patient_visit_schedule.patient
        palliative_phase = visit.get_palliative_phase_display()
        sugar = visit.general_random_blood_sugar
        pulse = visit.pulse
        blood_pressure = visit.blood_pressure
        notes = visit.notes
        context = {
            'date': visit.created_date.date().strftime("%d/%m/%Y"),
            'palliative_phase': palliative_phase,
            'sugar': sugar,
            'pulse': pulse,
            'blood_pressure': blood_pressure,
            'notes': notes,
        }
        relatives = patient.patientfamilymember_set.all()
        for relative in relatives:
            relative_email = relative.email
            if relative_email:
                send_mail(
                    "Arike - Patient Visit Details",
                    render_to_string('email_templates/relative_report.html', context),
                    "marmik@thedataboy.com",
                    [patient.nurse.email]
                )
                logger.info(f"Relative report sent to {patient.nurse.email}")
