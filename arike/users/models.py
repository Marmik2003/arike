import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

USER_ROLES = (
    ('dist_admin', 'District Admin'),
    ('pri_nurse', 'Primary Nurse'),
    ('sec_nurse', 'Secondary Nurse'),
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, email, password, **extra_fields):
        values = [email]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, email, password, **extra_fields)


class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    is_verified = models.BooleanField(default=False)
    district = models.ForeignKey('district_admin.District', null=True, blank=True, on_delete=models.PROTECT)
    facility = models.ForeignKey('district_admin.Facility', null=True, blank=True, on_delete=models.PROTECT)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    def get_role(self):
        return self.role


class NurseReportSetting(models.Model):
    nurse = models.OneToOneField(User, on_delete=models.CASCADE)
    is_report_enabled = models.BooleanField(default=False)
    report_time = models.TimeField(null=True, blank=True)
    last_sent_report_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.last_sent_report_time is None:
            self.last_sent_report_time = timezone.now().replace(
                hour=self.report_time.hour,
                minute=self.report_time.minute
            ) - datetime.timedelta(days=1)
        obj = super().save(*args, **kwargs)
        return obj
