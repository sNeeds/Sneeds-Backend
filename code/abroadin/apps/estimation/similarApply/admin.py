from django.contrib import admin

from . import models

from abroadin.apps.estimation.form.admin import StudentDetailedInfoBaseAdmin


class AppliedToInline(admin.TabularInline):
    model = models.AppliedTo
    extra = 1
    autocomplete_fields = ['university', 'major', ]


@admin.register(models.AppliedStudentDetailedInfo)
class AppliedStudentDetailedInfoAdmin(StudentDetailedInfoBaseAdmin):
    inlines = [AppliedToInline] + StudentDetailedInfoBaseAdmin.inlines
    list_display = ['id', 'student_name']
