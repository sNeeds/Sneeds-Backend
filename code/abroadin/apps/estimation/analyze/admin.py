from abroadin.apps.estimation.analyze.models import Chart, ChartItemData
from django.contrib import admin


class ChartItemDataInline(admin.TabularInline):
    model = ChartItemData
    extra = 1


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    inlines = [ChartItemDataInline]
