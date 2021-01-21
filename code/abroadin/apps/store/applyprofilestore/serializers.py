from rest_framework import serializers

from .models import ApplyProfileGroup

from abroadin.apps.applyprofile.models import ApplyProfile
from abroadin.apps.applyprofile.serializers import ApplyProfileSerializer


class ApplyProfileGroupRequestSerializer(serializers.ModelSerializer):
    apply_profiles = serializers.PrimaryKeyRelatedField(
        queryset=ApplyProfile.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
        many=True,
        read_only=True,
    )

    class Meta:
        model = ApplyProfileGroup
        fields = ['id', 'apply_profiles']

    def create(self, validated_data):
        instance = ApplyProfileGroup.objects.create_by_apply_profiles(validated_data)
        return instance

    def update(self, instance, validated_data):
        raise NotImplementedError("Update through this serializer is not allowed.")


class ApplyProfileGroupSerializer(serializers.ModelSerializer):
    apply_profiles = ApplyProfileSerializer()

    title = serializers.Field()
    subtitle = serializers.Field()

    class Meta:
        model = ApplyProfileGroup
        fields = ['id', 'apply_profiles', 'title', 'subtitle', 'price']

    def create(self, validated_data):
        raise NotImplementedError("Create through this serializer is not allowed.")

    def update(self, instance, validated_data):
        raise NotImplementedError("Update through this serializer is not allowed.")
