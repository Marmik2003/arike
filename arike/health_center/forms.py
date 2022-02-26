from django import forms

from arike.health_center.models import Patient, PatientFamilyMember, PatientDisease, PatientTreatment, TreatmentNote, \
    PatientVisitSchedule, PatientVisitDetail

input_classes = ' '.join([
    'block py-3 px-4',
    'w-full',
    'bg-gray-200 text-gray-700 border-gray-200',
    'border rounded',
    'py-3 px-4',
    'focus:outline-none focus:border-0 focus:ring-0',
])


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
