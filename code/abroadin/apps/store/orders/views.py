from rest_framework import  permissions

from abroadin.base.api import generics
from . import serializers
from .models import Order
from .permissions import OrderOwnerPermission


class OrderListView(generics.CListAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    ordering_fields = ['created', ]

    def get_queryset(self):
        user = self.request.user
        qs = Order.objects.filter(user=user)
        return qs


class OrderDetailView(generics.CRetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    lookup_field = 'id'
    permission_classes = (OrderOwnerPermission, permissions.IsAuthenticated)
