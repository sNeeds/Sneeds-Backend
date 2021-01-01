from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Cart
from ..storeBase.models import Product
from ..storeBase.serializers import ProductSerializer


class ProductsPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        print("to internal:", data)
        super().to_internal_value(data)

    def to_representation(self, value):
        print("Got repre1")
        return 123


class CartSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="cart:cart-detail", lookup_field='id', read_only=True)
    products = ProductsPrimaryKeyRelatedField(pk_field=IntegerField(), queryset=Product.objects.all(), many=True,
                                              required=False)

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
