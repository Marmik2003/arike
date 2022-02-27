import logging
from datetime import timedelta, datetime, time

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

from arike.users.models import NurseReportSetting
from arike.health_center.models import Patient, PatientTreatment, TreatmentNote, PatientDisease, PatientVisitSchedule

from config import celery_app


logger = logging.getLogger(__name__)
User = get_user_model()

today = timezone.now()
yesterday = today - timedelta(days=1)


@celery_app.task()
def send_daily_report():
    """Celery task that sends daily report to nurse."""
    with transaction.atomic():
        reports = NurseReportSetting.objects.select_for_update().filter(last_sent_report_time__lt=yesterday)
        for report in reports:
            user = User.objects.get(id=report.nurse.id)
            patients_count = Patient.objects.filter(nurse=user, created_date__gte=yesterday).count()
            yesterday_visits = PatientVisitSchedule.objects.filter(
                patient__nurse=user,
                visit_date__gte=yesterday,
                visit_date__lt=today
            ).count()
            patients_treated_count = PatientTreatment.objects.filter(given_by=user, created_date__gte=yesterday).count()
            patients_disease_count = PatientDisease.objects.filter(investigated_by=user, created_date__gte=yesterday)\
                .count()
            patients_notes_count = TreatmentNote.objects.filter(given_by=user, created_date__gte=yesterday).count()
            patients_treated_count += patients_notes_count
            today_visits = PatientVisitSchedule.objects.filter(
                visit_date__gte=today,
                visit_date__lte=today + timedelta(days=1),
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
