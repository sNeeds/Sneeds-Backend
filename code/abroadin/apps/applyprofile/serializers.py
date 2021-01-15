from rest_framework import serializers

from abroadin.apps.data.applydata.models import Publication
from abroadin.apps.data.applydata import serializers as data_serializers

from .models import ApplyProfile, Admission
from abroadin.apps.data.account.serializers import UniversitySerializer
from ..data.applydata.serializers import GradeSerializer

RELATED_CLASSES = [
    {
        'model_class': ApplyProfile,
        'hyperlink_view_name': 'applyprofile:apply-profile-detail',
        'hyperlink_lookup_field': 'object_id',
        'hyperlink_lookup_url_kwarg': 'id',
        'hyperlink_format': None
    },
]


class PublicationSerializer(data_serializers.PublicationSerializer):
    related_classes = RELATED_CLASSES

    class Meta(data_serializers.PublicationSerializer.Meta):
        abstract = False


class PublicationRequestSerializer(data_serializers.PublicationRequestSerializer):
    related_classes = RELATED_CLASSES

    class Meta(data_serializers.PublicationRequestSerializer.Meta):
        abstract = False

    def validate(self, attrs):
        return super().validate(attrs)


class EducationSerializer(data_serializers.EducationSerializer):
    related_classes = RELATED_CLASSES

    class Meta(data_serializers.EducationSerializer.Meta):
        abstract = False

    def validate(self, attrs):
        return super().validate(attrs)


class EducationRequestSerializer(data_serializers.EducationRequestSerializer):
    related_classes = RELATED_CLASSES

    class Meta(data_serializers.EducationRequestSerializer.Meta):
        pass

    def validate(self, attrs):
        return super().validate(attrs)


class AdmissionSerializer(serializers.ModelSerializer):
    home = UniversitySerializer()
    destination = UniversitySerializer()
    destination = GradeSerializer()
    class Meta:
        model = Admission
        fields = [
            'id', 'apply_profile', 'enroll_year', 'home', 'destination', 'grade',
            'scholarship', 'scholarship_unit', 'major', 'accepted', 'description',
        ]


class ApplyProfileSerializer(serializers.ModelSerializer):
    admissions = AdmissionSerializer(
        many=True,
    )

    publications = PublicationSerializer(
        many=True
    )

    educations = EducationSerializer(
        many=True,
    )

    # TODO change this to a more simple class without writing function
    language_certificates = serializers.SerializerMethodField(
        method_name='get_language_certificates',
    )

    class Meta:
        model = ApplyProfile
        fields = [
            'id', 'name', 'gap', 'admissions', 'publications', 'educations',
            'language_certificates',
        ]

    def get_language_certificates(self, obj):
        return data_serializers.serialize_language_certificates(obj.language_certificates.all(), self, RELATED_CLASSES)
