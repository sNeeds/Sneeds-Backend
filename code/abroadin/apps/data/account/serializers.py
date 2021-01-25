from django.contrib.auth import get_user_model
from rest_framework import serializers

from abroadin.base.values import AccessibilityTypeChoices
from . import models

User = get_user_model()


class CountrySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:country-detail",
        lookup_field='slug',
        read_only=True
    )

    class Meta:
        model = models.Country
        fields = ('id', 'url', 'name', 'slug', 'picture')


class LockedCountrySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, default="*", source=' ')
    url = serializers.CharField(read_only=True, default="*", source=' ')
    name = serializers.CharField(read_only=True, default="*", source=' ')
    slug = serializers.CharField(read_only=True, default="*", source=' ')
    picture = serializers.CharField(read_only=True, default="*", source=' ')

    class Meta:
        model = models.Country
        fields = ('id', 'url', 'name', 'slug', 'picture')


class UniversitySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:university-detail",
        lookup_field='id',
        read_only=True
    )
    country = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="account:country-detail",
        lookup_field='slug',
    )

    class Meta:
        model = models.University
        fields = ('id', 'url', 'name', 'country', 'description', 'picture')


class LockedUniversitySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, default="*", source=' ')
    url = serializers.CharField(read_only=True, default="*", source=' ')
    name = serializers.CharField(read_only=True, default="*", source=' ')
    country = LockedCountrySerializer()
    description = serializers.CharField(read_only=True, default="*", source=' ')
    picture = serializers.CharField(read_only=True, default="*", source=' ')

    accessibility_type = serializers.CharField(read_only=True, default=AccessibilityTypeChoices.LOCKED, source=' ')

    class Meta:
        model = models.University
        fields = ('id', 'url', 'name', 'country', 'description', 'picture',
                  'accessibility_type',
                  )



class MajorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:field-of-study-detail",
        lookup_field='id',
        read_only=True
    )

    class Meta:
        model = models.Major
        fields = ('id', 'url', 'name', 'description')


class LockedMajorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, default="*", source=' ')
    url = serializers.CharField(read_only=True, default="*", source=' ')
    name = serializers.CharField(read_only=True, default="*", source=' ')
    description = serializers.CharField(read_only=True, default="*", source=' ')
    accessibility_type = serializers.CharField(read_only=True, default=AccessibilityTypeChoices.LOCKED, source=' ')

    class Meta:
        model = models.Major
        fields = ('id', 'url', 'name', 'description',
                  'accessibility_type',
                  )
