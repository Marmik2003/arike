# Generated by Django 3.2.12 on 2022-02-25 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_center', '0004_alter_patientfamilymember_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientfamilymember',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other')], default='m', max_length=2),
            preserve_default=False,
        ),
    ]
