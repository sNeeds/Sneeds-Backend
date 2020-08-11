from django.contrib import admin
from django.db.models import Q
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware

from .models import Order
from advanced_filters.admin import AdminAdvancedFiltersMixin

from ..carts.models import Cart


@admin.register(Order)
class OrderAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ["order_id", "user", "total", "subtotal", "created"]
    fields = (
        ("order_id", "status"), "user", "sold_products", ("used_discount",
                                                          "time_slot_sales_number_discount"), ("subtotal", "total"),
        "created", "updated",

    )
    filter_horizontal = ('sold_products',)
    readonly_fields = ["order_id", "created", "updated"]
    advanced_filter_fields = (
        "total",
        "created"
    )
    date_hierarchy = 'created'

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        user = request.user

        if user.groups.all().filter(name="adminplus"):
            return qs.get_customs()

        elif request.user.is_superuser:
            return qs

        return qs.none()
