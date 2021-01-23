from rest_framework import serializers

from abroadin.apps.data.applydata import serializers as ad_serializers
from abroadin.apps.data.account import serializers as account_serializers

from abroadin.apps.store.applyprofilestore.utils import get_user_bought_apply_profiles

from .models import ApplyProfile, Admission
from ..data.account.models import University, Major
from ..data.applydata.models import Grade

RELATED_CLASSES = [
    {
        'model_class': ApplyProfile,
        'hyperlink_view_name': 'applyprofile:apply-profile-detail',
        'hyperlink_lookup_field': 'object_id',
        'hyperlink_lookup_url_kwarg': 'id',
        'hyperlink_format': None
    },
]


class AppSpecificPublicationSerializer(ad_serializers.PublicationSerializer):
    related_classes = RELATED_CLASSES

    class Meta(ad_serializers.PublicationSerializer.Meta):
        abstract = False


class AppSpecificEducationSerializer(ad_serializers.EducationSerializer):
    related_classes = RELATED_CLASSES

    class Meta(ad_serializers.EducationSerializer.Meta):
        abstract = False

    def validate(self, attrs):
        return super().validate(attrs)


class AdmissionSerializer(serializers.ModelSerializer):
    destination = account_serializers.UniversitySerializer()
    major = account_serializers.MajorSerializer()
    grade = ad_serializers.GradeSerializer()

    class Meta:
        model = Admission
        fields = [
            'id', 'apply_profile', 'enroll_year', 'destination',
            'scholarship', 'major', 'grade', 'accepted', 'description',
        ]


class LockedUniversitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(default="*")
    url = serializers.ReadOnlyField(default="*")
    name = serializers.ReadOnlyField(default="*")
    country = serializers.ReadOnlyField(default="*")
    description = serializers.ReadOnlyField(default="*")
    picture = serializers.ReadOnlyField(default="*")

    class Meta:
        model = University
        fields = ('id', 'url', 'name', 'country', 'description', 'picture')


class LockedMajorSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(default="*")
    url = serializers.ReadOnlyField(default="*")
    name = serializers.ReadOnlyField(default="*")
    description = serializers.ReadOnlyField(default="*")

    class Meta:
        model = Major
        fields = ('id', 'url', 'name', 'description')


class LockedGradeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(default="*")
    name = serializers.ReadOnlyField(default="*")

    class Meta:
        model = Grade
        fields = ["id", "name"]


class LockedAdmissionSerializer(serializers.ModelSerializer):
    destination = LockedUniversitySerializer()
    major = LockedMajorSerializer()
    grade = LockedGradeSerializer()

    enroll_year = serializers.ReadOnlyField(default="*")
    scholarship = serializers.ReadOnlyField(default="*")
    accepted = serializers.ReadOnlyField(default="*")
    description = serializers.ReadOnlyField(default="*")

    class Meta:
        model = Admission
        fields = [
            'id', 'apply_profile', 'enroll_year', 'destination',
            'scholarship', 'major', 'grade', 'accepted', 'description',
        ]


class ApplyProfileSerializer(serializers.ModelSerializer):

    admissions = serializers.SerializerMethodField(
        method_name="get_admissions"
    )

    publications = AppSpecificPublicationSerializer(
        many=True
    )

    educations = AppSpecificEducationSerializer(
        many=True,
    )

    # TODO change this to a more simple class without writing function
    language_certificates = serializers.SerializerMethodField(
        method_name='get_language_certificates',
    )

    class Meta:
        model = ApplyProfile
        fields = [
            'id', 'name', 'gap',
            'admissions',
            'publications', 'educations',
            'language_certificates',
        ]

    def represent_admissions(self, is_unlocked, admissions):
        if is_unlocked:
            return AdmissionSerializer(admissions)

        free_admissions = Admission.get_free_admissions(admissions)
        locked_admissions = Admission.get_locked_admissions(admissions, free_admissions)
        return AdmissionSerializer(free_admissions, many=True).data + LockedAdmissionSerializer(locked_admissions).data

    def get_admissions(self, obj):
        assert self.context is not None, "context is None"
        assert self.context.get('request') is not None, "context['request'] is None"

        user = self.context['request'].user
        is_unlocked_apply_profile = False
        if not user.is_authenticated:
            is_unlocked_apply_profile = False
        elif obj.id in get_user_bought_apply_profiles(user=user):
            is_unlocked_apply_profile = True

        return self.represent_admissions(is_unlocked_apply_profile, obj.adnissions)

    def get_language_certificates(self, obj):
        return ad_serializers.serialize_language_certificates(obj.language_certificates.all(), self, RELATED_CLASSES)
