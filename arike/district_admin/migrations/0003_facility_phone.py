# Generated by Django 3.2.12 on 2022-02-23 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('district_admin', '0002_auto_20220220_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
