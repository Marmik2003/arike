# Generated by Django 3.2.12 on 2022-02-25 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('health_center', '0008_treatment'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientTreatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('notes', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='health_center.patient')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='health_center.treatment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TreatmentNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('notes', models.TextField()),
                ('nurse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('patient_treatment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='health_center.patienttreatment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
