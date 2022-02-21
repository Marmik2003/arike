from django.db import models
from multiselectfield import MultiSelectField

from utils.models import BaseModel

# Create your models here.
GENDER_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Other')
)

PATIENT_RELATIONSHIPS = (
    ('brother', 'Brother'),
    ('sister', 'Sister'),
    ('husband', 'Husband'),
    ('wife', 'Wife'),
    ('father', 'Father'),
    ('mother', 'Mother'),
    ('son', 'Son'),
    ('daughter', 'Daughter'),
    ('uncle', 'Uncle'),
    ('aunt', 'Aunt'),
    ('nephew', 'Nephew'),
    ('niece', 'Niece'),
    ('cousin', 'Cousin'),
    ('other', 'Other')
)

PALLIATIVE_PHASES = (
    ('stable', 'Stable'),
    ('unstable', 'Unstable'),
    ('deteriotive', 'Deteriotive'),
    ('dying', 'Dying'),
)

SYSTEMIC_EXAMINATION_CHOICES = (
    ('cardiovascular', 'Cardiovascular'),
    ('gastrointestinal', 'Gastrointestinal'),
    ('respiratory', 'Respiratory'),
    ('genitourinary', 'Genital-urinary'),
)


class Disease(models.Model):
    name = models.CharField(max_length=50)
    icd_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Patient(BaseModel):
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    address = models.TextField()
    landmark = models.CharField(max_length=25)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    emergency_phone_number = models.CharField(max_length=15)
    expired_time = models.DateTimeField(null=True, blank=True)
    ward = models.ForeignKey('district_admin.Ward', on_delete=models.PROTECT)
    facility = models.ForeignKey('district_admin.Facility', on_delete=models.PROTECT)

    def __str__(self):
        return self.full_name


class PatientFamilyMember(BaseModel):
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT)
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    address = models.TextField()
    landmark = models.CharField(max_length=25)
    phone = models.CharField(max_length=15)
    relationship = models.CharField(max_length=20, choices=PATIENT_RELATIONSHIPS)
    education_level = models.CharField(max_length=20)
    occupation = models.CharField(max_length=50)
    remarks = models.TextField()
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class PatientDisease(BaseModel):
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT)
    disease = models.ForeignKey('Disease', on_delete=models.PROTECT)
    notes = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.disease.name


class PatientVisitSchedule(BaseModel):
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT)
    nurse = models.ForeignKey('users.User', on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()

    def __str__(self):
        return str(self.date)


class PatientVisitDetail(BaseModel):
    patient_visit_schedule = models.ForeignKey('PatientVisitSchedule', on_delete=models.PROTECT)
    palliative_phase = models.CharField(max_length=12)
    blood_pressure = models.CharField(max_length=10)
    pulse = models.IntegerField()
    general_random_blood_sugar = models.CharField(max_length=10)
    personal_hygiene = models.TextField()
    mouth_hygiene = models.TextField()
    public_hygiene = models.TextField()
    systemic_examination = models.CharField(max_length=20, choices=SYSTEMIC_EXAMINATION_CHOICES)
    patient_at_pease = models.BooleanField(default=False)
    pain = models.BooleanField(default=False)
    symptoms = MultiSelectField(choices=(('fever', 'Fever'), ('cough', 'Cough'), ('sore_throat', 'Sore throat'),))
    notes = models.TextField()

    def __str__(self):
        return str(self.patient_visit_schedule.date)
