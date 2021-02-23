from django.contrib import admin

from abroadin.apps.users.consultants.models import ConsultantProfile, StudyInfo


class StudyInfoInline(admin.TabularInline):
    model = StudyInfo
    extra = 1


@admin.register(ConsultantProfile)
class ConsultantProfileAdmin(admin.ModelAdmin):
    inlines = (StudyInfoInline,)
    readonly_fields = ["rate", ]
    list_display = ["id", "__str__", "user", "time_slot_price", "rate", "active", ]
