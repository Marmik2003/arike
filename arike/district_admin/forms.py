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


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['kind', 'name', 'address', 'ward', 'pincode', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kind'] = forms.ChoiceField(
            choices=FACILITY_KIND,
            widget=forms.RadioSelect(
                attrs={'class': 'form-radio text-green-600 h-5 w-5 focus:ring-0 focus:outline-none'}),
        )

        self.fields['name'].widget.attrs.update({'class': input_classes})
        self.fields['address'].widget.attrs.update({'class': input_classes})
        self.fields['ward'].widget.attrs.update({'class': input_classes})
        self.fields['pincode'].widget.attrs.update({'class': input_classes})
        self.fields['phone'].widget.attrs.update({'class': input_classes})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'facility', 'district', 'password']
