from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Cart
from ..storeBase.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="cart:cart-detail", lookup_field='id', read_only=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'url', 'user', 'products', 'subtotal', 'total', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request', None)
        user = request.user

        validated_data["user"] = user
        return super().create(validated_data)

    def validate_products(self, products):
        if not products:
            raise ValidationError("No products in cart")

        return products
