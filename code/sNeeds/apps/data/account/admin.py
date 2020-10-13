from django.contrib import admin

from . import models


@admin.register(models.University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rank', 'is_college']
    search_fields = ['name']


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', ]
    search_fields = ['name']


@admin.register(models.Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent_major', 'hierarchy_str']
    search_fields = ['name']
