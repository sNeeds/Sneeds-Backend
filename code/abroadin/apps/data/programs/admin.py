from froala_editor.widgets import FroalaEditor

from django.contrib import admin
from django.db.models import TextField

from . import models


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'grade']
    search_fields = ['name']
    formfield_overrides = {
        # https://github.com/froala/django-froala-editor/
        TextField: {'widget': FroalaEditor},
    }
