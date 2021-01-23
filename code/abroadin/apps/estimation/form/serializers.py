from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from abroadin.apps.data.applydata import models as ad_models
from abroadin.apps.data.applydata.serializers import serialize_language_certificates
from abroadin.apps.users.customAuth.serializers import SafeUserDataSerializer

from .models import WantToApply, StudentDetailedInfo, SDI_CT

LanguageCertificateType = ad_models.LanguageCertificate.LanguageCertificateType

RELATED_CLASSES = [
    {
        'model_class': StudentDetailedInfo,
        'hyperlink_view_name': 'estimation.form:student-detailed-info-detail',
        'hyperlink_lookup_field': 'object_id',
        'hyperlink_lookup_url_kwarg': 'id',
        'hyperlink_format': None
    }
]


class StudentDetailedInfoSerializer(serializers.ModelSerializer):

    user = SafeUserDataSerializer(read_only=True)
    regular_certificates = serializers.SerializerMethodField()
    want_to_applies = serializers.SerializerMethodField()

    # TODO change this to a more simple class without writing function
    language_certificates = serializers.SerializerMethodField(
        method_name='get_language_certificates',
    )
    educations = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()

    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user', 'age', 'gender', 'is_married', 'educations', 'publications',
            'regular_certificates', 'resume', 'related_work_experience', 'academic_break', 'olympiad',
            'created', 'updated', 'language_certificates', 'want_to_applies', 'payment_affordability',
            'prefers_full_fund', 'prefers_half_fund', 'prefers_self_fund',
            'comment', 'powerful_recommendation', 'linkedin_url', 'homepage_url',
        ]

    def create(self, validated_data):
        raise ValidationError(_("Create object through this serializer is not allowed"))

    def update(self, instance, validated_data):
        raise ValidationError(_("Update object through this serializer is not allowed"))

    def get_want_to_applies(self, obj):
        qs = WantToApply.objects.filter(student_detailed_info__id=obj.id)
        return WantToApplySerializer(qs, many=True, context=self.context).data

    def get_regular_certificates(self, obj):
        return self.get_certificates(obj, ad_models.RegularLanguageCertificate,
                                     AppSpecificRegularAppSpecificLanguageCertificateSerializer)

    def get_educations(self, obj):
        qs = ad_models.Education.objects.filter(
            content_type=SDI_CT, object_id=obj.id
        )
        return AppSpecificEducationSerializer(qs, many=True, context=self.context).data

    def get_publications(self, obj):
        qs = ad_models.Publication.objects.filter(
            content_type=SDI_CT, object_id=obj.id
        )
        return AppSpecificPublicationSerializer(qs, many=True, context=self.context).data

    def get_certificates(self, obj, model_class, serializer_class):
        qs = model_class.objects.filter(content_type=SDI_CT, object_id=obj.id)
        return serializer_class(qs, many=True, context=self.context).data

    def get_language_certificates(self, obj):
        return serialize_language_certificates(
            obj.language_certificates.all(), self, RELATED_CLASSES)


class StudentDetailedInfoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user',
            'age', 'is_married',
            'payment_affordability', 'gender',
            'prefers_full_fund', 'prefers_half_fund', 'prefers_self_fund',
            'comment', 'resume', 'related_work_experience', 'academic_break',
            'olympiad', 'powerful_recommendation',
            'linkedin_url', 'homepage_url',
            'created', 'updated',
        ]

    def validate(self, attrs):
        return attrs


class StudentDetailedInfoCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetailedInfo
        fields = '__all__'

    def create(self, validated_data):
        return StudentDetailedInfo(**validated_data)
