# Generated by Django 3.2.12 on 2022-02-25 08:54

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('health_center', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientvisitdetail',
            name='symptoms',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('fever', 'Fever'), ('cough', 'Cough'), ('sore_throat', 'Sore throat'), ('headache', 'Headache'), ('diarrhea', 'Diarrhea'), ('vomiting', 'Vomiting'), ('nausea', 'Nausea'), ('abdominal_pain', 'Abdominal pain'), ('chest_pain', 'Chest pain'), ('shortness_of_breath', 'Shortness of breath'), ('other', 'Other')], max_length=109),
        ),
    ]
