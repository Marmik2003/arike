from django import forms

from arike.health_center.models import Patient, PatientFamilyMember, PatientDisease

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
