from django import forms
from django.db import transaction

from arike.health_center.models import Patient, PatientFamilyMember, PatientDisease, PatientTreatment, TreatmentNote, \
    PatientVisitSchedule, PatientVisitDetail
from arike.users.tasks import User, NurseReportSetting


input_classes = ' '.join([
    'block py-3 px-4',
    'w-full',
    'bg-gray-200 text-gray-700 border-gray-200',
    'border rounded',
    'py-3 px-4',
    'focus:outline-none focus:border-0 focus:ring-0',
])


class ProfileForm(forms.ModelForm):
    old_password = forms.CharField(
        label='Old password',
        widget=forms.PasswordInput(
            attrs={
                'class': input_classes,
                'placeholder': 'Old password',
            }
        ),
        required=False,
    )
    new_password = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(
            attrs={
                'class': input_classes,
                'placeholder': 'New password',
            }
        ),
        required=False,
    )
    confirm_password = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(
            attrs={
                'class': input_classes,
                'placeholder': 'Confirm password',
            }
        ),
        required=False,
    )
    enable_email_report = forms.BooleanField(
        label='Enable email report',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-checkbox h-6 w-6 rounded text-green-500 border-0 bg-slate-100'
            }
        ),
        required=False,
    )

    report_time = forms.TimeField(
        label='Report time',
        widget=forms.TimeInput(
            attrs={
                'class': input_classes,
                'placeholder': 'Report time',
                'type': 'time',
            },
        ),
        required=False,
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': input_classes}),
            'last_name': forms.TextInput(attrs={'class': input_classes}),
            'email': forms.TextInput(attrs={'class': input_classes}),
            'phone_number': forms.TextInput(attrs={'class': input_classes}),
        }

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password) and old_password:
            raise forms.ValidationError('Old password is incorrect')
        return old_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return confirm_password

    def clean_report_time(self):
        report_time = self.cleaned_data.get('report_time')
        enable_email_report = self.cleaned_data.get('enable_email_report')
        if report_time and enable_email_report:
            report_time = report_time.strftime('%H:%M')
        return report_time

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('old_password'):
            user.set_password(self.cleaned_data['new_password'])
        if commit:
            if self.cleaned_data.get('report_time', None):
                with transaction.atomic():
                    user.save()
                    report, created = NurseReportSetting.objects.get_or_create(
                        nurse=user,
                    )
                    report.is_report_enabled = self.cleaned_data.get('enable_email_report')
                    report.report_time = self.cleaned_data.get('report_time')
                    report.save()
            else:
                user.save()
        return user


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'full_name', 'date_of_birth', 'address', 'landmark', 'phone', 'gender', 'emergency_phone_number',
            'expired_time',
        ]
        widgets = {
            'date_of_birth': forms.widgets.DateInput(attrs={'type': 'date'}),
            'expired_time': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': input_classes})


class PatientFamilyMemberForm(forms.ModelForm):
    class Meta:
        model = PatientFamilyMember
        fields = [
            'full_name', 'relationship', 'date_of_birth', 'gender', 'landmark', 'address',
            'phone', 'email', 'education_level', 'occupation', 'remarks',
        ]
        widgets = {
            'date_of_birth': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': input_classes})


class PatientDiseaseForm(forms.ModelForm):
    class Meta:
        model = PatientDisease
        fields = ['disease', 'notes', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': input_classes})


class PatientTreatmentForm(forms.ModelForm):
    class Meta:
        model = PatientTreatment
        fields = ['treatment', 'disease', 'notes', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': input_classes})

        self.fields['is_active'] = forms.BooleanField(
            widget=forms.CheckboxInput(
                attrs={
                    'class': 'form-checkbox h-6 w-6 rounded text-green-500 border-0 bg-slate-100'
                }
            ),
            required=False
        )


class TreatmentNoteForm(forms.ModelForm):
    class Meta:
        model = TreatmentNote
        fields = ['notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': input_classes})


class PatientVisitScheduleForm(forms.ModelForm):
    class Meta:
        model = PatientVisitSchedule
        fields = ['date', 'duration']
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': input_classes})


class PatientVisitDetailForm(forms.ModelForm):
    class Meta:
        model = PatientVisitDetail
        fields = [
            'palliative_phase', 'blood_pressure', 'general_random_blood_sugar',
            'pulse', 'personal_hygiene', 'mouth_hygiene', 'public_hygiene',
            'systemic_examination', 'symptoms', 'notes', 'patient_at_pease'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': input_classes})
        self.fields['patient_at_pease'] = forms.BooleanField(
            widget=forms.CheckboxInput(
                attrs={
                    'class': 'form-checkbox h-6 w-6 rounded text-green-500 border-0 bg-slate-100'
                }
            )
        )
