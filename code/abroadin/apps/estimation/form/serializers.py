from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from rest_framework import serializers

from abroadin.apps.data.applydata import models as ad_models
from abroadin.apps.data.applydata.serializers import SemesterYearSerializer, GradeSerializer, \
    EducationDetailedRepresentationSerializer, PublicationSerializer, LanguageCertificateInheritedSerializer
from abroadin.base.factory.class_factory import exclude_meta_fields_class_factory
from abroadin.apps.users.customAuth.serializers import SafeUserDataSerializer
from abroadin.apps.data.applydata.models import Education, Publication, LanguageCertificate
from abroadin.apps.data.globaldata.serializers import CountrySerializer, UniversitySerializer, MajorSerializer

from .models import WantToApply, StudentDetailedInfo

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


class WantToApplyBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WantToApply
        fields = [
            'id', 'countries', 'student_detailed_info',
            'universities', 'grades', 'majors', 'semester_years',
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        context = {"request": self.context.get("request")}

        ret["countries"] = CountrySerializer(instance.countries, context=context, many=True).data
        ret["universities"] = UniversitySerializer(instance.universities, context=context, many=True).data
        ret["grades"] = GradeSerializer(instance.grades, context=context, many=True).data
        ret["majors"] = MajorSerializer(instance.majors, context=context, many=True).data
        ret["semester_years"] = SemesterYearSerializer(instance.semester_years, context=context, many=True).data

        return ret


class StudentDetailedInfoSerializer(
    serializers.ModelSerializer
):
    exclude_fields = {"content_type", "object_id"}
    WantToApplyValidationSerializer = exclude_meta_fields_class_factory(
        WantToApplyBaseSerializer, exclude_fields={"student_detailed_info"}
    )
    EducationValidationSerializer = exclude_meta_fields_class_factory(
        EducationDetailedRepresentationSerializer, exclude_fields
    )
    PublicationValidationSerializer = exclude_meta_fields_class_factory(
        PublicationSerializer, exclude_fields
    )

    user = SafeUserDataSerializer(read_only=True)
    want_to_apply = WantToApplyValidationSerializer()
    educations = EducationValidationSerializer(many=True)
    publications = PublicationValidationSerializer(many=True)
    language_certificates = LanguageCertificateInheritedSerializer(many=True)

    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user', 'age', 'gender', 'is_married',
            'resume', 'related_work_experience', 'academic_break', 'olympiad',
            'created', 'updated', 'want_to_apply', 'educations', 'publications', 'language_certificates',
            'payment_affordability', 'prefers_full_fund', 'prefers_half_fund', 'prefers_self_fund',
            'comment', 'powerful_recommendation', 'linkedin_url', 'homepage_url',
        ]

    @transaction.atomic()
    def create(self, validated_data):
        want_to_apply_data = validated_data.pop('want_to_apply')
        educations_data = validated_data.pop('educations')
        publications_data = validated_data.pop('publications')
        language_certificates_data = validated_data.pop('language_certificates')

        form = StudentDetailedInfo.objects.create(**validated_data)
        form_content_type = ContentType.objects.get(app_label="form", model="studentdetailedinfo")

        want_to_apply_data['student_detailed_info'] = form
        WantToApply.objects.create_with_m2m(**want_to_apply_data)

        for data in educations_data:
            data['object_id'] = form.id
            data['content_type'] = form_content_type
            Education.objects.create_with_m2m(**data)

        for data in publications_data:
            data['object_id'] = form.id
            data['content_type'] = form_content_type
            Publication.objects.create_with_m2m(**data)

        for type_data in language_certificates_data:
            content_type = type_data['class_type']
            data = type_data['data']

            data['object_id'] = form.id
            data['content_type'] = form_content_type

            CertificateClass = content_type.model_class()
            CertificateClass.objects.create_with_m2m(**data)

        return form

    @transaction.atomic()
    def update(self, instance, validated_data):
        want_to_apply_data = validated_data.pop('want_to_apply', None)
        educations_data = validated_data.pop('educations', None)
        publications_data = validated_data.pop('publications', None)
        language_certificates_data = validated_data.pop('language_certificates', None)

        sdi_content_type = ContentType.objects.get(app_label="form", model="studentdetailedinfo")

        if want_to_apply_data:
            # print(want_to_apply_data)
            # WantToApply.objects.get(student_detailed_info=instance)
            # want_to_apply_data['student_detailed_info'] = instance
            # sdi_wta = instance.want_to_apply
            # want_to_apply_serializer = WantToApplyBaseSerializer(
            #     sdi_wta, data=want_to_apply_data, partial=True
            # )
            # if want_to_apply_serializer.is_valid(raise_exception=True):
            #     want_to_apply_serializer.save()
            sdi_wta = instance.want_to_apply
            sdi_wta.delete()
            want_to_apply_data['student_detailed_info'] = instance
            WantToApply.objects.create_with_m2m(**want_to_apply_data)

        if educations_data:
            Education.objects.filter(content_type=sdi_content_type, object_id=instance.id).delete()
            for data in educations_data:
                data['object_id'] = instance.id
                data['content_type'] = sdi_content_type
                Education.objects.create_with_m2m(**data)

        if publications_data:
            Publication.objects.filter(content_type=sdi_content_type, object_id=instance.id).delete()
            for data in publications_data:
                data['object_id'] = instance.id
                data['content_type'] = sdi_content_type
                Publication.objects.create_with_m2m(**data)

        if language_certificates_data:
            LanguageCertificate.objects.filter(content_type=sdi_content_type, object_id=instance.id).delete()
            for type_data in language_certificates_data:
                content_type = type_data['class_type']
                data = type_data['data']
                data['object_id'] = instance.id
                data['content_type'] = sdi_content_type
                CertificateClass = content_type.model_class()
                CertificateClass.objects.create_with_m2m(**data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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
