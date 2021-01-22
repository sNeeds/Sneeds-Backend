from rest_framework import serializers

from abroadin.apps.data.applydata import serializers as ad_serializers
from abroadin.apps.data.account import serializers as account_serializers

from .models import ApplyProfile, Admission

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


class AppSpecificPublicationRequestSerializer(ad_serializers.PublicationRequestSerializer):
    related_classes = RELATED_CLASSES

    class Meta(ad_serializers.PublicationRequestSerializer.Meta):
        abstract = False

    def validate(self, attrs):
        return super().validate(attrs)


class AppSpecificEducationSerializer(ad_serializers.EducationSerializer):
    related_classes = RELATED_CLASSES

    class Meta(ad_serializers.EducationSerializer.Meta):
        abstract = False

    def validate(self, attrs):
        return super().validate(attrs)


class AppSpecificEducationRequestSerializer(ad_serializers.EducationRequestSerializer):
    related_classes = RELATED_CLASSES

    class Meta(ad_serializers.EducationRequestSerializer.Meta):
        pass

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


class ApplyProfileSerializer(serializers.ModelSerializer):
    admissions = AdmissionSerializer(
        many=True,
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

    def get_language_certificates(self, obj):
        return ad_serializers.serialize_language_certificates(obj.language_certificates.all(), self, RELATED_CLASSES)
