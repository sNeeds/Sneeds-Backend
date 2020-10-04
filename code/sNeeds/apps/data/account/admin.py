from django.contrib import admin

from . import models

admin.site.register(models.Country)
admin.site.register(models.Major)


@admin.register(models.University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rank', 'is_college']
    search_fields = ['name']


