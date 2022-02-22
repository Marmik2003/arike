from django import forms

from arike.district_admin.models import Facility


class FacilityForm(forms.ModelForm):
    model = Facility
    fields = ['kind', 'name', 'address', 'ward', 'pincode']
