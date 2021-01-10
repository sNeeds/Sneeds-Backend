from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Cart
from ..storeBase.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="carts:cart-detail", lookup_field='id', read_only=True)
    products_detail = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'url', 'user', 'products', 'products_detail', 'subtotal', 'total', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'products_detail': {'read_only': True},
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

    def get_products_detail(self, obj):
        return ProductSerializer(obj.products.all().cast_subclasses(), many=True).data
