from django.contrib import admin

from .models import Order


#TODO: Removed AdminAdvancedFiltersMixin, check if working
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "order_id", "user", "total", "subtotal", "created"]
    fields = (
        ("order_id", "status"), "user", "sold_products", ("used_discount",
        "time_slot_sales_number_discount"), ("subtotal", "total"), "created", "updated",

    )
    filter_horizontal = ('sold_products',)
    readonly_fields = ["order_id", "created", "updated"]
    advanced_filter_fields = (
        "total",
        "created"
    )
    date_hierarchy = 'created'
