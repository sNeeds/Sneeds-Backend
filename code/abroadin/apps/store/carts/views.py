from rest_framework import permissions

from abroadin.base.api import generics

from . import serializers
from .models import Cart
from .permissions import CartOwnerPermission


class CartListView(generics.CListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartDetailView(generics.CRetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializer
    lookup_field = 'id'
    # permission_classes = (CartOwnerPermission, permissions.IsAuthenticated)
