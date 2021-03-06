# Generated by Django 3.2.12 on 2022-02-27 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='NurseReportSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_report_enabled', models.BooleanField(default=False)),
                ('report_time', models.TimeField(blank=True, null=True)),
                ('last_sent_report_time', models.DateTimeField(blank=True, null=True)),
                ('nurse', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
