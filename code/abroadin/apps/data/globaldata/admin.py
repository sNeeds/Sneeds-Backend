# https://github.com/froala/django-froala-editor/
from froala_editor.widgets import FroalaEditor

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import TextField

from . import models


class AddressInline(GenericTabularInline):
    model = models.Address
    extra = 1


class SocialInline(GenericTabularInline):
    model = models.Social
    extra = 1


@admin.register(models.University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rank', 'country', 'is_college']
    search_fields = ['name']
    inlines = [
        AddressInline,
        SocialInline,
    ]
    formfield_overrides = {
        # https://github.com/froala/django-froala-editor/
        TextField: {'widget': FroalaEditor},
    }


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', ]
    search_fields = ['name']


@admin.register(models.Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'hierarchy_str']
    search_fields = ['name']
