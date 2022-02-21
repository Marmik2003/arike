from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('phone_number', 'email', 'is_active',)
    list_filter = ('phone_number', 'email', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('role', 'is_verified', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'password1', 'password2',)}
         ),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('role', 'is_verified', 'is_active',)}),
    )
    search_fields = ('phone_number', 'email')
    ordering = ('phone_number', 'email',)
    view_on_site = False


admin.site.register(User, CustomUserAdmin)
