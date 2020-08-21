from django.contrib import admin

from . import models

from sNeeds.apps.account.admin import StudentDetailedInfoBaseAdmin


@admin.register(models.AppliedStudentDetailedInfo)
class AppliedStudentDetailedInfoAdmin(StudentDetailedInfoBaseAdmin):
    pass
