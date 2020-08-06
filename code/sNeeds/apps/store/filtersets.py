from django_filters import rest_framework as filters, DateTimeFromToRangeFilter, DateTimeFilter

from . import models


class TimeSlotSaleFilter(filters.FilterSet):
    start_time = DateTimeFilter(lookup_expr='gte')
    end_time = DateTimeFilter(lookup_expr='lte')
    price = filters.RangeFilter(field_name="price")

    class Meta:
        model = models.TimeSlotSale
        fields = [
            'consultant', 'price', 'start_time', 'end_time'
        ]
