from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from rangefilter.filter import DateTimeRangeFilter

from abroadin.utils.custom.admin.actions import export_as_csv_action
from .models import CustomUser, StudentProfile
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ['date_last_action', 'date_joined', 'last_login']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'is_email_verified')}),
        (_('Permissions'), {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'date_last_action')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    list_filter = (
        'is_email_verified',
        'is_staff',
        ('date_last_action', DateTimeRangeFilter),
        ('date_joined', DateTimeRangeFilter),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'get_full_name', 'is_email_verified', 'user_type', 'is_staff', 'date_last_action', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)

    actions = [
        export_as_csv_action("CSV Export", fields=['first_name', 'last_name', 'email', 'phone_number', 'user_type'])
    ]


admin.site.register(StudentProfile)
