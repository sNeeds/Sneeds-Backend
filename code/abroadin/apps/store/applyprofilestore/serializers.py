from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from .models import ApplyProfileGroup, SoldApplyProfileGroup

from abroadin.apps.applyprofile.models import ApplyProfile
from abroadin.apps.applyprofile.serializers import ApplyProfileSerializer
from .validators import validate_apply_profiles

User = get_user_model()


class ApplyProfileGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyProfileGroup
        fields = ['id', 'apply_profiles', 'user', 'title', 'subtitle', 'price']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        instance = ApplyProfileGroup.objects.create_with_apply_profiles(**validated_data)
        return instance

    def update(self, instance, validated_data):
        raise NotImplementedError("Update through this serializer is not allowed.")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        context = {"request": self.context.get("request")}

        ret["apply_profiles"] = ApplyProfileSerializer(instance.apply_profiles, context=context, many=True).data

        return ret


class SoldApplyProfileGroupSerializer(serializers.ModelSerializer):
    apply_profiles = ApplyProfileSerializer(
        many=True
    )

    title = serializers.CharField()
    subtitle = serializers.CharField()

    class Meta:
        model = SoldApplyProfileGroup
        fields = ['id', 'apply_profiles', 'title', 'subtitle', 'price']

    def create(self, validated_data):
        raise NotImplementedError("Create through this serializer is not allowed.")

    def update(self, instance, validated_data):
        raise NotImplementedError("Update through this serializer is not allowed.")
