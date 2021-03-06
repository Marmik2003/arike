from django.contrib.auth.forms import AuthenticationForm, UsernameField, ReadOnlyPasswordHashField
from django import forms

from arike.users.models import User


input_classes = ' '.join([
    'block py-3 px-4',
    'w-full',
    'bg-gray-200 text-gray-700 border-gray-200',
    'border rounded',
    'py-3 px-4',
    'focus:outline-none focus:border-0 focus:ring-0',
])


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0',
        }
    ))


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'phone_number', 'email', 'first_name', 'last_name',
            'role', 'is_verified', 'is_staff', 'is_superuser'
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"../password/\">this form</a>.")
    )

    class Meta:
        model = User
        fields = (
            'phone_number', 'email', 'first_name', 'last_name', 'role',
            'is_verified', 'password', 'is_active', 'is_superuser'
        )

    def clean_password(self):
        return self.initial["password"]


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': input_classes}),
        strip=False,
    )
    password2 = forms.CharField(
        label="Confirm password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': input_classes}),
    )

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
