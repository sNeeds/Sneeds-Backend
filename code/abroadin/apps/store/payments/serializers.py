from zeep import Client

from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PaymentVerifySerializer(serializers.Serializer):
    status = serializers.CharField(required=True)
    authority = serializers.CharField(min_length=36, max_length=36, required=True)

    def validate_status(self, value):
        if value not in ["OK", "NOK"]:
            raise serializers.ValidationError("Value should be OK or NOK")
        return value
