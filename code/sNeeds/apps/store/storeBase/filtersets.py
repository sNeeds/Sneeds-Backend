from django_filters import rest_framework as filters, DateTimeFilter

from . import models


class TimeSlotFilter(filters.FilterSet):
    start_time = DateTimeFilter(lookup_expr='gte')
    end_time = DateTimeFilter(lookup_expr='lte')
    price = filters.RangeFilter(field_name="price")

    class Meta:
        fields = [
            'consultant', 'price', 'start_time', 'end_time'
        ]


class TimeSlotSaleFilter(TimeSlotFilter):
    class Meta(TimeSlotFilter.Meta):
        model = models.TimeSlotSale


class SoldTimeSlotSaleFilter(TimeSlotFilter):
    class Meta(TimeSlotFilter.Meta):
        model = models.SoldTimeSlotSale
        fields = TimeSlotFilter.Meta.fields + ['used']