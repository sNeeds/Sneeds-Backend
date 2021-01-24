from rest_framework import serializers

from abroadin.apps.data.applydata import serializers as ad_serializers
from abroadin.apps.data.account import serializers as account_serializers

from abroadin.apps.store.applyprofilestore.utils import get_user_bought_apply_profiles

from .models import ApplyProfile, Admission
from ..data.account.serializers import LockedUniversitySerializer, LockedMajorSerializer
from ..data.applydata.serializers import LockedGradeSerializer
from ...base.values import AccessibilityTypeChoices

RELATED_CLASSES = [
    {
        'model_class': ApplyProfile,
        'hyperlink_view_name': 'applyprofile:apply-profile-detail',
        'hyperlink_lookup_field': 'object_id',
        'hyperlink_lookup_url_kwarg': 'id',
        'hyperlink_format': None
    },
]


class FullPublicationSerializer(ad_serializers.PublicationSerializer):
    related_classes = RELATED_CLASSES

    accessibility_type = serializers.CharField(read_only=True, default=AccessibilityTypeChoices.UNLOCKED, source=' ')

    class Meta(ad_serializers.PublicationSerializer.Meta):
        fields = ad_serializers.PublicationSerializer.Meta.fields + ['accessibility_type']


class FullEducationSerializer(ad_serializers.EducationSerializer):
    related_classes = RELATED_CLASSES

    accessibility_type = serializers.CharField(read_only=True, default=AccessibilityTypeChoices.UNLOCKED, source=' ')

    class Meta(ad_serializers.EducationSerializer.Meta):
        fields = ad_serializers.EducationSerializer.Meta.fields + ['accessibility_type']

    def validate(self, attrs):
        return super().validate(attrs)


class PartialEducationSerializer(ad_serializers.EducationSerializer):
    related_classes = RELATED_CLASSES

    accessibility_type = serializers.CharField(read_only=True, default=AccessibilityTypeChoices.UNLOCKED, source=' ')

    class Meta(ad_serializers.EducationSerializer.Meta):
        fields = [
            'id', 'university', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
            'content_type', 'object_id',
            'accessibility_type'
        ]

    def validate(self, attrs):
        return super().validate(attrs)


class LockedEducationSerializer(ad_serializers.EducationSerializer):
    related_classes = RELATED_CLASSES

    id = serializers.CharField(read_only=True, default="*", source=' ')
    university = LockedUniversitySerializer()
    grade = LockedGradeSerializer()
    major = LockedMajorSerializer()
    graduate_in = serializers.CharField(read_only=True, default="*", source=' ')
    thesis_title = serializers.CharField(read_only=True, default="*", source=' ')
    gpa = serializers.CharField(read_only=True, default="*", source=' ')
    content_type = serializers.CharField(read_only=True, default="*", source=' ')
    object_id = serializers.CharField(read_only=True, default="*", source=' ')

    accessibility_type = serializers.CharField(read_only=True, default=AccessibilityTypeChoices.LOCKED, source=' ')

    class Meta(ad_serializers.EducationSerializer.Meta):
        fields = [
            'id', 'university', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
            'content_type', 'object_id',
            'accessibility_type',
        ]

    def validate(self, attrs):
        return super().validate(attrs)


class FullAdmissionSerializer(serializers.ModelSerializer):
    """
    Full and unlocked serializer
    """
    destination = account_serializers.UniversitySerializer()
    major = account_serializers.MajorSerializer()
    grade = ad_serializers.GradeSerializer()
    accessibility_type = serializers.CharField(read_only=True, default=AccessibilityTypeChoices.UNLOCKED, source=' ')

    class Meta:
        model = Admission
        fields = [
            'id', 'apply_profile', 'enroll_year', 'destination',
            'scholarship', 'major', 'grade', 'accepted', 'description',
            'accessibility_type',
        ]


class PartialAdmissionSerializer(FullAdmissionSerializer):
    """
    Free admissions serializer. Just some fields are shown.
    """
    grade = serializers.CharField(read_only=True, default="*", source=' ')
    scholarship = serializers.CharField(read_only=True, default="*", source=' ')
    description = serializers.CharField(read_only=True, default="*", source=' ')

    accessibility_type = serializers.CharField(read_only=True, default=AccessibilityTypeChoices.PARTIAL, source=' ')

    class Meta:
        model = Admission
        fields = [
            'id', 'apply_profile', 'enroll_year', 'destination',
            'scholarship', 'major', 'grade', 'accepted', 'description',
            'accessibility_type'
        ]


class LockedAdmissionSerializer(serializers.ModelSerializer):
    """
    Locked Admission Serializer. All fields are hidden.
    """
    id = serializers.CharField(read_only=True, default="*", source=' ')
    destination = LockedUniversitySerializer()
    major = LockedMajorSerializer()
    grade = LockedGradeSerializer()

    enroll_year = serializers.CharField(read_only=True, default="*", source=' ')
    scholarship = serializers.CharField(read_only=True, default="*", source=' ')
    accepted = serializers.CharField(read_only=True, default="*", source=' ')
    description = serializers.CharField(read_only=True, default="*", source=' ')

    accessibility_type = serializers.CharField(read_only=True, default=AccessibilityTypeChoices.LOCKED, source=' ')

    class Meta:
        model = Admission
        fields = [
            'id', 'apply_profile', 'enroll_year', 'destination',
            'scholarship', 'major', 'grade', 'accepted', 'description',
            'accessibility_type',
        ]


class ApplyProfileSerializer(serializers.ModelSerializer):
    user_bought_apply_profiles_id = []

    accessibility_type = serializers.SerializerMethodField(
        method_name='get_accessibility_type'
    )

    admissions = serializers.SerializerMethodField(
        method_name="get_admissions"
    )

    publications = serializers.SerializerMethodField(
        method_name="get_publications"
    )

    educations = serializers.SerializerMethodField(
        method_name="get_educations"
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
            'accessibility_type',
        ]

    def to_representation(self, instance):
        self.clear_local_cache()
        return super().to_representation(instance)

    def clear_local_cache(self):
        self.user_bought_apply_profiles_id = None

    def _is_unlocked(self, obj):
        assert self.context is not None, "context is None"
        assert self.context.get('request') is not None, "context['request'] is None"

        user = self.context['request'].user
        is_unlocked_apply_profile = False
        if not user.is_authenticated:
            is_unlocked_apply_profile = False
            return is_unlocked_apply_profile

        if self.user_bought_apply_profiles_id is None:
            self.user_bought_apply_profiles_id = get_user_bought_apply_profiles(user=user).values_list('id', flat=True)

        if obj.id in self.user_bought_apply_profiles_id:
            is_unlocked_apply_profile = True
        return is_unlocked_apply_profile

    def get_accessibility_type(self, obj):
        if self._is_unlocked(obj):
            return AccessibilityTypeChoices.UNLOCKED
        return AccessibilityTypeChoices.PARTIAL

    def get_admissions(self, obj):
        return self.represent_admissions(obj, self._is_unlocked(obj))

    def represent_admissions(self, obj, is_unlocked,):
        if is_unlocked:
            objects = FullAdmissionSerializer(obj.admissions.all(), many=True, context=self.context).data
            accessibility_type = AccessibilityTypeChoices.UNLOCKED

        else:
            free_admissions, locked_admissions = obj.get_free_locked_admissions()
            objects = PartialAdmissionSerializer(free_admissions, many=True, context=self.context).data + \
                      LockedAdmissionSerializer(locked_admissions, many=True, context=self.context).data
            accessibility_type = AccessibilityTypeChoices.PARTIAL

        return {'accessibility_type': accessibility_type, 'objects': objects}

    def get_publications(self, obj):
        return self.represent_publications(obj, self._is_unlocked(obj))

    def represent_publications(self, obj, is_unlocked,):
        if is_unlocked:
            objects = FullPublicationSerializer(obj.publications.all(), many=True, context=self.context).data
            accessibility_type = AccessibilityTypeChoices.UNLOCKED
        else:
            objects = []
            accessibility_type = AccessibilityTypeChoices.LOCKED

        return {'accessibility_type': accessibility_type, 'objects': objects}

    def get_educations(self, obj):
        return self.represent_educations(obj, self._is_unlocked(obj))

    def represent_educations(self, obj, is_unlocked,):
        if is_unlocked:
            objects = FullEducationSerializer(obj.educations.all(), many=True, context=self.context).data
            accessibility_type = AccessibilityTypeChoices.UNLOCKED
        else:
            free_educations, locked_educations = obj.get_free_locked_educations()
            objects = PartialEducationSerializer(free_educations, many=True, context=self.context).data + \
                      LockedEducationSerializer(locked_educations, many=True, context=self.context).data
            accessibility_type = AccessibilityTypeChoices.PARTIAL

        return {'accessibility_type': accessibility_type, 'objects': objects}

    def get_language_certificates(self, obj):
        return self.represent_language_certificates(obj, self._is_unlocked(obj))

    def represent_language_certificates(self, obj, is_unlocked,):
        if is_unlocked:
            objects = serialize_language_certificates(obj.language_certificates.all(), self, RELATED_CLASSES)
            accessibility_type = AccessibilityTypeChoices.UNLOCKED
        else:
            free_educations, locked_educations = obj.get_free_locked_educations()
            objects = PartialEducationSerializer(free_educations, many=True, context=self.context).data + \
                      LockedEducationSerializer(locked_educations, many=True, context=self.context).data
            accessibility_type = AccessibilityTypeChoices.PARTIAL

        return {'accessibility_type': accessibility_type, 'objects': objects}


def serialize_language_certificates(queryset, parent_serializer, related_classes):
    return ad_serializers.serialize_language_certificates(queryset, parent_serializer, related_classes)
