from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Order

from abroadin.apps.store.carts.models import Cart
from abroadin.apps.store.storeBase.serializers import SoldTimeSlotSaleSerializer
from abroadin.apps.store.storePackages.serializers import SoldStorePaidPackagePhaseSerializer


class OrderSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="store.order:order-detail", lookup_field='id', read_only=True)
    title = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'url', 'title', 'order_id', 'status', 'subtotal', 'total', 'created', 'updated',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'url': {'read_only': True},
            'title': {'read_only': True},
            'order_id': {'read_only': True},
            'status': {'read_only': True},
            'subtotal': {'read_only': True},
            'total': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
        }

    def get_title(self, obj):
        return "Similar Admissions"

    def validate(self, attrs):
        user = self.context.get('request', None).user

        order_qs = Order.objects.filter(cart__user=user)
        if order_qs.count() > 0:
            raise ValidationError({"detail": "User has an active order."})

        return attrs

    def create(self, validated_data):
        user = None
        request = self.context.get('request', None)

        if request and hasattr(request, "user"):
            user = request.user

        try:
            cart = Cart.objects.get(user=user)
        except:
            raise ValidationError({"detail": _("User has no cart.")})

        order_obj = Order.objects.create(cart=cart)

        return order_obj
