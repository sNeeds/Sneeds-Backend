from django.contrib import admin

from . import models


@admin.register(models.ApplyProfileGroup)
class ApplyProfileGroup(admin.ModelAdmin):
    filter_horizontal = ('apply_profiles',)


@admin.register(models.SoldApplyProfileGroup)
class SoldApplyProfileGroup(admin.ModelAdmin):
    filter_horizontal = ('apply_profiles',)
