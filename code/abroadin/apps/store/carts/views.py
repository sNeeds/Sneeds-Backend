from rest_framework import permissions

from abroadin.base.api import generics

from . import serializers
from .models import Cart
from .permissions import CartOwnerPermission


class CartListView(generics.CListCreateAPIView):
    queryset = Cart.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CartDetailView(generics.CRetrieveAPIView):
    lookup_field = 'id'
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializer
    permission_classes = (CartOwnerPermission, permissions.IsAuthenticated,)
