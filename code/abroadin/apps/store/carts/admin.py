from django.contrib import admin

from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ['subtotal', 'total']
    list_display = ['id', 'user', 'created', 'updated']