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
    id = serializers.CharField(read_only=True, default="*", source=' ')
    url = serializers.CharField(read_only=True, default="*", source=' ')
    name = serializers.CharField(read_only=True, default="*", source=' ')
    country = serializers.CharField(read_only=True, default="*", source=' ')
    description = serializers.CharField(read_only=True, default="*", source=' ')
    picture = serializers.CharField(read_only=True, default="*", source=' ')

    class Meta:
        model = University
        fields = ('id', 'url', 'name', 'country', 'description', 'picture')


class LockedMajorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, default="*", source=' ')
    url = serializers.CharField(read_only=True, default="*", source=' ')
    name = serializers.CharField(read_only=True, default="*", source=' ')
    description = serializers.CharField(read_only=True, default="*", source=' ')

    class Meta:
        model = Major
        fields = ('id', 'url', 'name', 'description')


class LockedGradeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, default="*", source=' ')
    name = serializers.CharField(read_only=True, default="*", source=' ')

    class Meta:
        model = Grade
        fields = ["id", "name"]


class LockedAdmissionSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True, default="*", source=' ')
    destination = LockedUniversitySerializer()
    major = LockedMajorSerializer()
    grade = LockedGradeSerializer()

    enroll_year = serializers.CharField(read_only=True, default="*", source=' ')
    scholarship = serializers.CharField(read_only=True, default="*", source=' ')
    accepted = serializers.CharField(read_only=True, default="*", source=' ')
    description = serializers.CharField(read_only=True, default="*", source=' ')

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
            return AdmissionSerializer(admissions, many=True, context=self.context).data

        free_admissions = Admission.get_free_admissions(admissions)
        locked_admissions = Admission.get_locked_admissions(admissions, free_admissions)
        return AdmissionSerializer(free_admissions, many=True, context=self.context).data +\
               LockedAdmissionSerializer(locked_admissions, many=True, context=self.context).data

    def get_admissions(self, obj):
        assert self.context is not None, "context is None"
        assert self.context.get('request') is not None, "context['request'] is None"

        user = self.context['request'].user
        is_unlocked_apply_profile = False
        if not user.is_authenticated:
            is_unlocked_apply_profile = False
        elif obj.id in get_user_bought_apply_profiles(user=user).values_list('id', flat=True):
            is_unlocked_apply_profile = True

        return self.represent_admissions(is_unlocked_apply_profile, obj.admissions)

    def get_language_certificates(self, obj):
        return ad_serializers.serialize_language_certificates(obj.language_certificates.all(), self, RELATED_CLASSES)
