from rest_framework import  permissions
from rest_framework.response import Response

from abroadin.base.api import generics
from abroadin.utils.custom.custom_permissions import IsConsultantUnsafePermission
from abroadin.apps.users.consultants.models import ConsultantProfile

from . import serializers
from . import filtersets
from .models import TimeSlotSale, SoldTimeSlotSale
from .permissions import (
    TimeSlotSaleOwnerPermission,
    SoldTimeSlotSaleOwnerPermission,
)


class TimeSlotSaleListAPIView(generics.CListCreateAPIView):
    queryset = TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    filterset_class = filtersets.TimeSlotSaleFilter
    permission_classes = [IsConsultantUnsafePermission, permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'GET':
            serializer_class = serializers.ShortTimeSlotSaleSerializer

        return serializer_class


class TimeSlotSaleExistListAPIView(generics.CListAPIView):
    queryset = TimeSlotSale.objects.all()
    filterset_class = filtersets.TimeSlotSaleFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.exists():
            return Response({"exists": True, "number": len(queryset)})
        return Response({"exists": False, "number": len(queryset)})


class TimeSlotSaleDetailAPIView(generics.CRetrieveDestroyAPIView):
    lookup_field = "id"
    queryset = TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    permission_classes = [TimeSlotSaleOwnerPermission, permissions.IsAuthenticatedOrReadOnly]


class SoldTimeSlotSaleListAPIView(generics.CListAPIView):
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


class SoldTimeSlotSaleDetailAPIView(generics.CRetrieveAPIView):
    lookup_field = "id"
    queryset = SoldTimeSlotSale.objects.all()
    serializer_class = serializers.SoldTimeSlotSaleSerializer
    permission_classes = [SoldTimeSlotSaleOwnerPermission, permissions.IsAuthenticated]


class SoldTimeSlotSaleSafeListAPIView(generics.CListAPIView):
    queryset = SoldTimeSlotSale.objects.all()
    serializer_class = serializers.ShortSoldTimeSlotSaleSafeSerializer
    filterset_class = filtersets.SoldTimeSlotSaleFilter
    ordering_fields = ['start_time', ]


class SoldTimeSlotSaleSafeDetailAPIView(generics.CRetrieveAPIView):
    lookup_field = 'id'
    queryset = SoldTimeSlotSale.objects.all()
    serializer_class = serializers.SoldTimeSlotSaleSafeSerializer
