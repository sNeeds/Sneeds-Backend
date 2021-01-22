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


class ApplyProfileGroupRequestSerializer(serializers.ModelSerializer):
    apply_profiles = serializers.PrimaryKeyRelatedField(
        queryset=ApplyProfile.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
        many=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
        many=False,
    )

    class Meta:
        model = ApplyProfileGroup
        fields = ['id', 'apply_profiles', 'user']

    def validate_apply_profiles(self, value):
        try:
            return validate_apply_profiles(value)
        except Exception as e:
            raise ValidationError(_(e.message))

    def validate_user(self, value):
        request: Request = self.context.get("request")
        if request and hasattr(request, "user"):
            if value != request.user:
                raise ValidationError(_("User is not the user mentioned in data"))
            return value
        else:
            raise ValidationError(_("Can't validate data.Can't get request user."))

    def create(self, validated_data):
        instance = ApplyProfileGroup.objects.create_by_apply_profiles(**validated_data)
        return instance

    def update(self, instance, validated_data):
        raise NotImplementedError("Update through this serializer is not allowed.")


class ApplyProfileGroupSerializer(serializers.ModelSerializer):
    apply_profiles = ApplyProfileSerializer(
        many=True
    )

    title = serializers.CharField()
    subtitle = serializers.CharField()

    class Meta:
        model = ApplyProfileGroup
        fields = ['id', 'apply_profiles', 'title', 'subtitle', 'price']

    def create(self, validated_data):
        raise NotImplementedError("Create through this serializer is not allowed.")

    def update(self, instance, validated_data):
        raise NotImplementedError("Update through this serializer is not allowed.")


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
