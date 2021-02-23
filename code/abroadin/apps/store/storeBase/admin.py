from django.contrib import admin
from .models import Product
from ..orders.models import Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["real_type", ]