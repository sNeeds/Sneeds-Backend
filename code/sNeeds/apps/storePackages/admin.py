from django.contrib import admin

from .models import (
    StorePackage, StorePackagePhase, SoldStorePackage, StorePackagePhaseThrough,
    SoldStoreUnpaidPackagePhase, SoldStorePaidPackagePhase, SoldStorePackagePhaseDetail,
    ConsultantSoldStorePackageAcceptRequest, StorePackagePhaseDetail
)
from ..orders.models import Order


class StorePackagePhaseThroughInline(admin.TabularInline):
    model = StorePackagePhaseThrough
    extra = 1


@admin.register(StorePackage)
class StorePackageAdmin(admin.ModelAdmin):
    inlines = (StorePackagePhaseThroughInline,)
    readonly_fields = ["price", "total_price", ]
    list_display = ["id", "title", "total_price"]


@admin.register(SoldStorePackage)
class SoldStorePackageAdmin(admin.ModelAdmin):
    readonly_fields = ["paid_price", "total_price", ]
    list_display = ['id', 'title', 'sold_to', 'consultant', 'created', 'updated']
    readonly_fields = ('created', 'updated')

    def get_list_display(self, request):
        if request.user.groups.all().filter(name="adminplus"):
            return ['title', 'sold_to', 'consultant', 'created', 'updated']
        return self.list_display

    def get_queryset(self, request):
        qs = super(SoldStorePackageAdmin, self).get_queryset(request)
        user = request.user

        if user.groups.all().filter(name="adminplus"):
            new_qs = qs.none()
            for order in Order.objects.all().get_customs():
                new_qs = new_qs | qs.filter(id__in=order.sold_products.all().values_list('id', flat=True))
            return new_qs

        elif request.user.is_superuser:
            return qs

        return qs.none()


@admin.register(SoldStoreUnpaidPackagePhase)
class SoldStoreUnpaidPackagePhaseAdmin(admin.ModelAdmin):
    readonly_fields = ['status', 'sold_store_package', ]
    list_display = ['id', 'title', 'price', 'sold_store_package', ]


@admin.register(SoldStorePaidPackagePhase)
class SoldStorePaidPackagePhaseAdmin(admin.ModelAdmin):
    exclude = ['sold_to', ]
    readonly_fields = ['status', 'sold_store_package', ]
    list_display = ['id', 'title', 'price', 'sold_store_package', ]
    readonly_fields = ('created', 'updated')


@admin.register(StorePackagePhase)
class StorePackagePhaseAdmin(admin.ModelAdmin):
    filter_horizontal = ['phase_details', ]


@admin.register(ConsultantSoldStorePackageAcceptRequest)
class ConsultantSoldStorePackageAcceptRequestAdmin(admin.ModelAdmin):
    list_display = ['sold_store_package', 'consultant', 'get_sold_store_package_sold_to', 'created']
    list_filter = ['sold_store_package', 'consultant', ]


admin.site.register(StorePackagePhaseDetail)
admin.site.register(SoldStorePackagePhaseDetail)
