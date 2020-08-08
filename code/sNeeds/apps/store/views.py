from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, generics, mixins, permissions, filters
from rest_framework.response import Response

from . import serializers
from . import filtersets
from .models import TimeSlotSale, SoldTimeSlotSale, Product
from .permissions import (
    TimeSlotSaleOwnerPermission,
    SoldTimeSlotSaleOwnerPermission,
)
from ...utils.custom.custom_permissions import IsConsultantUnsafePermission
from ..consultants.models import ConsultantProfile


class TimeSlotSaleListAPIView(generics.ListCreateAPIView):
    queryset = TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    filterset_class = filtersets.TimeSlotSaleFilter
    permission_classes = [IsConsultantUnsafePermission, permissions.IsAuthenticatedOrReadOnly]


class TimeSlotSaleExistListAPIView(generics.ListAPIView):
    queryset = TimeSlotSale.objects.all()
    filterset_class = filtersets.TimeSlotSaleFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if self.queryset.exists():
            return Response({"exists": True, "number": len(queryset)})
        return Response({"exists": False, "number": len(queryset)})


class TimeSlotSaleDetailAPIView(generics.RetrieveDestroyAPIView):
    lookup_field = "id"
    queryset = TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    permission_classes = [TimeSlotSaleOwnerPermission, permissions.IsAuthenticatedOrReadOnly]


class SoldTimeSlotSaleListAPIView(generics.ListAPIView):
    queryset = SoldTimeSlotSale.objects.all()
    serializer_class = serializers.SoldTimeSlotSaleSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['start_time', ]
    filterset_fields = ['used', 'consultant']

    def get_queryset(self):
        user = self.request.user
        consultant_profile_qs = ConsultantProfile.objects.filter(user=user)

        if consultant_profile_qs.exists():
            consultant_profile = consultant_profile_qs.first()
            return SoldTimeSlotSale.objects.filter(consultant=consultant_profile).order_by('start_time')
        else:
            return SoldTimeSlotSale.objects.filter(sold_to=user).order_by('start_time')


class SoldTimeSlotSaleDetailAPIView(generics.RetrieveAPIView):
    lookup_field = "id"
    queryset = SoldTimeSlotSale.objects.all()
    serializer_class = serializers.SoldTimeSlotSaleSerializer
    permission_classes = [SoldTimeSlotSaleOwnerPermission, permissions.IsAuthenticated]


class SoldTimeSlotSaleSafeListAPIView(generics.ListAPIView):
    queryset = SoldTimeSlotSale.objects.all()
    serializer_class = serializers.SoldTimeSlotSaleSafeSerializer
    filterset_class = filtersets.SoldTimeSlotSaleFilter
    ordering_fields = ['start_time', ]


class SoldTimeSlotSaleSafeDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = SoldTimeSlotSale.objects.all()
    serializer_class = serializers.SoldTimeSlotSaleSafeSerializer
