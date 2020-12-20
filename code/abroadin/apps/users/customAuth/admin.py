from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from rangefilter.filter import DateTimeRangeFilter

from abroadin.utils.custom.admin.actions import export_as_csv_action
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from .models import CustomUser, StudentProfile
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ['date_last_action', 'date_joined', 'last_login']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'is_email_verified',
                                         'receive_marketing_email')}),
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
    list_display = (
        'email', 'has_form', 'get_full_name', 'is_email_verified', 'user_type', 'is_staff', 'date_last_action',
        'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)

    actions = [
        export_as_csv_action(
            "CSV Export",
            fields=['email', 'phone_number', 'get_full_name', 'is_email_verified', 'user_type', 'is_staff',
                    'date_last_action', 'date_joined', 'has_form', 'home_university']
        )
    ]

    def has_form(self, obj):
        return StudentDetailedInfo.objects.filter(user__id=obj.id).exists()

    def home_university(self, obj):
        try:
            form = StudentDetailedInfo.objects.get(user__id=obj.id)
        except StudentDetailedInfo.DoesNotExist:
            return None

        university_through_qs = form.university_through_qs()
        if not university_through_qs.exists():
            return None

        last_grade = university_through_qs.order_by_grade().last()

        return last_grade.university


admin.site.register(StudentProfile)
