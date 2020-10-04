from rest_framework import serializers

import sNeeds.apps
from sNeeds.apps.data.account.serializers import UniversitySerializer, MajorSerializer, CountrySerializer
from sNeeds.apps.users.consultants.models import StudyInfo, ConsultantProfile
from sNeeds.apps.data.account.models import Country


class VeryShortConsultantProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ConsultantProfile
        fields = (
            'first_name',
            'last_name',
        )

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name


class ShortConsultantProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="consultant:consultant-profile-detail",
        lookup_field='slug',
        read_only=True
    )
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ConsultantProfile
        fields = (
            'id',
            'slug',
            'url',
            'profile_picture',
            'first_name',
            'last_name',
        )

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name


class ConsultantProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="consultant:consultant-profile-detail",
        lookup_field='slug',
        read_only=True
    )
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    rate = serializers.SerializerMethodField(read_only=True)
    study_info = serializers.SerializerMethodField()

    class Meta:
        model = ConsultantProfile
        ordering = ['-rate']
        fields = (
            'id', 'url', 'bio', 'profile_picture', 'first_name', 'last_name',
            'study_info', 'slug', 'aparat_link', 'resume', 'time_slot_price', 'rate', 'active')

    def get_rate(self, obj):
        rate = obj.rate
        if rate is None:
            rate = 4.5 + (obj.id % 10) / 20
        else:
            rate = (1 * 5 + obj.rate) / 2
        rate = round(rate, 1)
        return rate

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_study_info(self, obj):
        qs = StudyInfo.objects.filter(consultant__id=obj.id)
        return StudyInfoSerializer(qs, many=True, context=self.context).data


class StudyInfoSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    major = MajorSerializer(read_only=True)
    country = serializers.SerializerMethodField()

    class Meta:
        model = sNeeds.apps.users.consultants.models.StudyInfo
        fields = ('id', 'university', 'major', 'country', 'grade')

    def get_country(self, obj):
        if obj.university.country:
            qs = Country.objects.get(id=obj.university.country.id)
            return CountrySerializer(qs, context=self.context).data
        return None
