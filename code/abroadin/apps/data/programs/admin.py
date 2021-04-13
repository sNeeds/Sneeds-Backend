from froala_editor.widgets import FroalaEditor

from django.contrib import admin
from django.db.models import TextField

from . import models
from .models import ProgramIntake, ProgramOtherFee, ProgramRequirement, ProgramOtherRequirement

admin.site.register(ProgramOtherFee)
admin.site.register(ProgramOtherRequirement)


class ProgramIntakeInline(admin.TabularInline):
    model = ProgramIntake
    extra = 1


class ProgramRequirementInline(admin.TabularInline):
    model = ProgramRequirement
    extra = 1


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'grade']
    search_fields = ['name']
    inlines = [
        ProgramIntakeInline,
        ProgramRequirementInline
    ]
    formfield_overrides = {
        # https://github.com/froala/django-froala-editor/
        TextField: {'widget': FroalaEditor},
    }
