# Generated by Django 3.2.12 on 2022-02-26 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_center', '0012_patienttreatment_disease'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientvisitdetail',
            name='pain',
        ),
    ]