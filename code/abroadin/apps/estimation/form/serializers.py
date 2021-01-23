from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from rest_framework import serializers

from abroadin.apps.data.applydata import models as ad_models
from abroadin.apps.data.applydata.serializers import SemesterYearSerializer, GradeSerializer, EducationSerializer, \
    EducationDetailedRepresentationSerializer
from abroadin.apps.users.customAuth.serializers import SafeUserDataSerializer

from .models import WantToApply, StudentDetailedInfo
from abroadin.apps.data.account.serializers import CountrySerializer, UniversitySerializer, MajorSerializer
from ...data.applydata.models import Education

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
            'id', 'student_detailed_info', 'countries',
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


class WantToApplyValidationSerializer(WantToApplyBaseSerializer):
    class Meta(WantToApplyBaseSerializer.Meta):
        extra_kwargs = {
            "student_detailed_info": {"read_only": True}
        }


class EducationValidationSerializer(EducationDetailedRepresentationSerializer):
    class Meta(EducationDetailedRepresentationSerializer.Meta):
        fields = list(set(EducationDetailedRepresentationSerializer.Meta.fields) - {"content_type", "object_id"})


class StudentDetailedInfoSerializer(serializers.ModelSerializer):
    user = SafeUserDataSerializer(read_only=True)
    want_to_apply = WantToApplyValidationSerializer()
    educations = EducationValidationSerializer(many=True)

    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user', 'age', 'gender', 'is_married',
            'resume', 'related_work_experience', 'academic_break', 'olympiad',
            'created', 'updated', 'want_to_apply', 'educations',
            'payment_affordability', 'prefers_full_fund', 'prefers_half_fund', 'prefers_self_fund',
            'comment', 'powerful_recommendation', 'linkedin_url', 'homepage_url',
        ]

    def validate(self, attrs):
        return attrs

    @transaction.atomic()
    def create(self, validated_data):
        want_to_apply_data = validated_data.pop('want_to_apply')
        educations_data = validated_data.pop('educations')

        form = StudentDetailedInfo.objects.create(**validated_data)
        SDI_content_type = ContentType.objects.get(app_label="form", model="studentdetailedinfo")

        want_to_apply_data['student_detailed_info'] = form
        WantToApply.objects.create_with_m2m(**want_to_apply_data)

        for data in educations_data:
            data['object_id'] = form.id
            data['content_type'] = SDI_content_type
            Education.objects.create_with_m2m(**data)

        return form


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
