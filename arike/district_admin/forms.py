from django import forms

from arike.district_admin.models import Facility, FACILITY_KIND
from arike.users.models import User

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

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('old_password'):
            user.set_password(self.cleaned_data['new_password'])
        if commit:
            user.save()
        return user


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['kind', 'chc', 'name', 'address', 'ward', 'pincode', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kind'] = forms.ChoiceField(
            choices=FACILITY_KIND,
            widget=forms.RadioSelect(
                attrs={'class': 'form-radio text-green-600 h-5 w-5 focus:ring-0 focus:outline-none'}),
        )
        self.fields['chc'].widget.attrs.update({'class': input_classes})
        self.fields['name'].widget.attrs.update({'class': input_classes})
        self.fields['address'].widget.attrs.update({'class': input_classes})
        self.fields['ward'].widget.attrs.update({'class': input_classes})
        self.fields['pincode'].widget.attrs.update({'class': input_classes})
        self.fields['phone'].widget.attrs.update({'class': input_classes})

        if 'ward' in self.data:
            try:
                ward = int(self.data.get('ward'))
                self.fields['chc'].queryset = Facility.objects.filter(ward=ward, kind='chc')
            except (ValueError, TypeError):
                pass


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'facility']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': input_classes})
        self.fields['last_name'].widget.attrs.update({'class': input_classes})
        self.fields['email'].widget.attrs.update({'class': input_classes})
        self.fields['phone_number'].widget.attrs.update({'class': input_classes})
        self.fields['role'].widget.attrs.update({'class': input_classes})
        self.fields['role'].choices = [('', 'Select Role')] +\
                                      [(choice[0], choice[1]) for choice in self.fields['role'].choices[2:]]
        self.fields['facility'].widget.attrs.update({'class': input_classes, 'required': 'required'})

        if 'ward' in self.data:
            try:
                ward = int(self.data.get('ward'))
                self.fields['facility'].queryset = Facility.objects.filter(ward_id=ward)
            except (ValueError, TypeError):
                pass

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('role') == 'pri_nurse' and cleaned_data.get('facility').kind != 'phc':
            raise forms.ValidationError('Primary Nurse can only be assigned to PHC')
        if cleaned_data.get('role') == 'sec_nurse' and cleaned_data.get('facility').kind != 'chc':
            raise forms.ValidationError('Secondary Nurse can only be assigned to CHC')
        return cleaned_data
