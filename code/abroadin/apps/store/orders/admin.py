from django.contrib import admin

from .models import Order


#TODO: Removed AdminAdvancedFiltersMixin, check if working
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "order_id", "user", "total", "subtotal", "created"]
    fields = (
        ("order_id", "status"), "user", "sold_products", ("subtotal", "total"),
        "created", "updated",

    )
    filter_horizontal = ('sold_products',)
    readonly_fields = ["order_id", "created", "updated"]
    advanced_filter_fields = (
        "total",
        "created"
    )
    date_hierarchy = 'created'

    def get_list_display(self, request):
        if request.user.groups.all().filter(name="adminplus"):
            return ["order_id", "user", "total", "subtotal", "created"]
        return self.list_display

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        user = request.user

        if user.groups.all().filter(name="adminplus"):
            return qs.get_customs()

        elif request.user.is_superuser:
            return qs

        return qs.none()
