from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import abroadin.apps
import abroadin.apps.data.applydata.models
from abroadin.apps.data.account import models
from abroadin.apps.data.account.models import BasicFormField
from abroadin.apps.data.account.serializers import CountrySerializer, UniversitySerializer, MajorSerializer

from abroadin.apps.data.applydata import serializers as ad_serializers

from .models import SemesterYear, WantToApply, StudentDetailedInfo, Publication, Grade

from ...data.applydata.models import Education

LanguageCertificateType = abroadin.apps.estimation.form.models.LanguageCertificate.LanguageCertificateType

RELATED_CLASSES = [
    {
        'model_class': StudentDetailedInfo,
        'hyperlink_view_name': 'estimation.form:student-detailed-info-detail',
        'hyperlink_lookup_field': 'object_id',
        'hyperlink_lookup_url_kwarg': 'id',
        'hyperlink_format': None
    }
]


class BasicFormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicFormField
        fields = ['id', 'name']


class SemesterYearSerializer(ad_serializers.SemesterYearSerializer):
    class Meta(ad_serializers.SemesterYearSerializer.Meta):
        pass


class GradeSerializer(ad_serializers.GradeSerializer):
    class Meta(ad_serializers.GradeSerializer):
        pass


class WantToApplySerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True)
    universities = UniversitySerializer(many=True)
    majors = MajorSerializer(many=True)
    semester_years = ad_serializers.SemesterYearSerializer(many=True)
    grades = ad_serializers.GradeSerializer(many=True)

    class Meta:
        model = WantToApply
        fields = [
            'id', 'student_detailed_info', 'countries', 'universities', 'grades', 'majors', 'semester_years',
        ]

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class WantToApplyRequestSerializer(serializers.ModelSerializer):
    student_detailed_info = serializers.PrimaryKeyRelatedField(
        queryset=abroadin.apps.estimation.form.models.StudentDetailedInfo.objects.all(),
        pk_field=serializers.UUIDField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )
    countries = serializers.PrimaryKeyRelatedField(
        queryset=models.Country.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
        many=True,
    )
    universities = serializers.PrimaryKeyRelatedField(
        queryset=models.University.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=True,
        allow_empty=True,
        required=False,
        many=True,
    )

    majors = serializers.PrimaryKeyRelatedField(
        queryset=models.Major.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=True,
        allow_empty=True,
        required=False,
        many=True
    )
    semester_years = serializers.PrimaryKeyRelatedField(
        queryset=abroadin.apps.estimation.form.models.SemesterYear.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=True,
        allow_empty=True,
        required=False,
        many=True
    )

    class Meta:
        model = abroadin.apps.estimation.form.models.WantToApply
        fields = [
            'id', 'student_detailed_info', 'countries', 'universities',
            'grades', 'majors', 'semester_years',
        ]

    def create(self, validated_data):
        student_detailed_info = validated_data.get("student_detailed_info")
        sdi_want_to_applies_qs = WantToApply.objects.filter(student_detailed_info__id=student_detailed_info.id)
        if sdi_want_to_applies_qs.exists():
            raise ValidationError(_("Student detailed info form already has a want to apply object assigned to it."))
        return super().create(validated_data)

    def validate(self, attrs):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_user = request.user
            student_detailed_info = attrs.get("student_detailed_info")
            if student_detailed_info.user is not None and student_detailed_info.user != request_user:
                raise ValidationError(_("User can't set student_detailed_info of another user."))
            if student_detailed_info.user is None and request_user.is_authenticated:
                raise ValidationError(_("User can't set student_detailed_info of another user."))
        else:
            raise ValidationError(_("Can't validate data.Can't get request user."))
        return attrs


class PublicationSerializer(ad_serializers.PublicationSerializer):
    related_classes = RELATED_CLASSES

    class Meta(ad_serializers.PublicationSerializer.Meta):
        pass

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class PublicationRequestSerializer(ad_serializers.PublicationRequestSerializer):
    related_classes = RELATED_CLASSES

    class Meta(ad_serializers.PublicationRequestSerializer.Meta):
        pass

    def validate(self, attrs):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_user = request.user
            student_detailed_info = attrs.get("student_detailed_info")
            if student_detailed_info.user is not None and student_detailed_info.user != request_user:
                raise ValidationError(_("User can't set student_detailed_info of another user."))
            if student_detailed_info.user is None and request_user.is_authenticated:
                raise ValidationError(_("User can't set student_detailed_info of another user."))
        else:
            raise ValidationError(_("Can't validate data.Can't get request user."))
        return attrs


class EducationSerializer(ad_serializers.EducationSerializer):
    related_classes = RELATED_CLASSES

    class Meta(ad_serializers.EducationSerializer.Meta):
        pass

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class EducationRequestSerializer(ad_serializers.EducationRequestSerializer):
    related_classes = RELATED_CLASSES

    class Meta(ad_serializers.EducationRequestSerializer.Meta):
        pass

    def validate(self, attrs):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_user = request.user
            student_detailed_info = attrs.get("student_detailed_info")
            if student_detailed_info.user is not None and student_detailed_info.user != request_user:
                raise ValidationError(_("User can't set student_detailed_info of another user."))
            if student_detailed_info.user is None and request_user.is_authenticated:
                raise ValidationError(_("User can't set student_detailed_info of another user."))
        else:
            raise ValidationError(_("Can't validate data.Can't get request user."))
        return attrs


class LanguageCertificateSerializer(ad_serializers.LanguageCertificateSerializer):
    related_classes = RELATED_CLASSES

    class Meta(ad_serializers.LanguageCertificateSerializer.Meta):
        pass

    def validate(self, attrs):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_user = request.user
            student_detailed_info = attrs.get("student_detailed_info")
            if student_detailed_info.user is not None and student_detailed_info.user != request_user:
                raise ValidationError(
                    {'student_detailed_info': _("User can't set student_detailed_info of another user.")})
            if student_detailed_info.user is None and request_user.is_authenticated:
                raise ValidationError(
                    {'student_detailed_info': _("User can't set student_detailed_info of another user.")})
        else:
            raise ValidationError(_("Can't validate data.Can't get request user."))
        return super().validate(attrs)


class RegularLanguageCertificateSerializer(LanguageCertificateSerializer,
                                           ad_serializers.RegularLanguageCertificateSerializer):
    related_classes = RELATED_CLASSES

    class Meta(ad_serializers.RegularLanguageCertificateSerializer.Meta):
        pass


class GMATCertificateSerializer(LanguageCertificateSerializer, ad_serializers.GMATCertificateSerializer):
    class Meta(ad_serializers.GMATCertificateSerializer):
        pass


class GREGeneralCertificateSerializer(LanguageCertificateSerializer, ad_serializers.GREGeneralCertificateSerializer):
    class Meta(ad_serializers.GREGeneralCertificateSerializer.Meta):
        pass


class GRESubjectCertificateSerializer(LanguageCertificateSerializer, ad_serializers.GRESubjectCertificateSerializer):
    class Meta(ad_serializers.GRESubjectCertificateSerializer.Meta):
        pass


class GREBiologyCertificateSerializer(LanguageCertificateSerializer, ad_serializers.GREBiologyCertificateSerializer):
    class Meta(ad_serializers.GREBiologyCertificateSerializer.Meta):
        pass


class GREPhysicsCertificateSerializer(LanguageCertificateSerializer, ad_serializers.GREPhysicsCertificateSerializer):
    class Meta(ad_serializers.GREPhysicsCertificateSerializer.Meta):
        pass


class GREPsychologyCertificateSerializer(LanguageCertificateSerializer,
                                         ad_serializers.GREPsychologyCertificateSerializer):
    class Meta(ad_serializers.GREPsychologyCertificateSerializer):
        pass


class DuolingoCertificateSerializer(LanguageCertificateSerializer, ad_serializers.DuolingoCertificateSerializer):
    class Meta(ad_serializers.DuolingoCertificateSerializer.Meta):
        pass


class StudentDetailedInfoBaseSerializer(serializers.ModelSerializer):
    regular_certificates = serializers.SerializerMethodField()
    gmat_certificates = serializers.SerializerMethodField()
    gre_general_certificates = serializers.SerializerMethodField()
    gre_subject_certificates = serializers.SerializerMethodField()
    gre_biology_certificates = serializers.SerializerMethodField()
    gre_physics_certificates = serializers.SerializerMethodField()
    gre_psychology_certificates = serializers.SerializerMethodField()
    duolingo_certificates = serializers.SerializerMethodField()

    universities = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()

    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'universities', 'publications',
            'regular_certificates', 'gmat_certificates', 'gre_general_certificates', 'gre_subject_certificates',
            'gre_biology_certificates', 'gre_physics_certificates', 'gre_psychology_certificates',
            'duolingo_certificates',
            'resume', 'related_work_experience', 'academic_break', 'olympiad',
            'created', 'updated',
        ]

    def get_regular_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.data.applydata.models.RegularLanguageCertificate,
                                     RegularLanguageCertificateSerializer)

    def get_gmat_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.data.applydata.models.GMATCertificate,
                                     GMATCertificateSerializer)

    def get_gre_general_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.data.applydata.models.GREGeneralCertificate,
                                     GREGeneralCertificateSerializer)

    def get_gre_subject_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.data.applydata.models.GRESubjectCertificate,
                                     GRESubjectCertificateSerializer)

    def get_gre_biology_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.data.applydata.models.GREBiologyCertificate,
                                     GREBiologyCertificateSerializer)

    def get_gre_physics_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.data.applydata.models.GREPhysicsCertificate,
                                     GREPhysicsCertificateSerializer)

    def get_gre_psychology_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.data.applydata.models.GREPsychologyCertificate,
                                     GREPsychologyCertificateSerializer)

    def get_duolingo_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.data.applydata.models.DuolingoCertificate,
                                     DuolingoCertificateSerializer)

    def get_universities(self, obj):
        # return 'a'
        # TODO
        # print(type(obj.id))
        qs = Education.objects.filter(
            content_type=ContentType.objects.get_for_model(obj.__class__),
            object_id=str(obj.id),
            # student_detailed_info__id=obj.id
        )
        return EducationSerializer(qs, many=True, context=self.context).data

    def get_publications(self, obj):
        # return 'a'
        # TODO
        qs = Publication.objects.filter(
            content_type=ContentType.objects.get_for_model(obj.__class__),
            object_id=str(obj.id),
            # student_detailed_info__id=obj.id
        )
        return PublicationSerializer(qs, many=True, context=True).data

    def create(self, validated_data):
        raise ValidationError(_("Create object through this serializer is not allowed"))

    def update(self, instance, validated_data):
        raise ValidationError(_("Update object through this serializer is not allowed"))

    # Custom method
    def get_certificates(self, obj, model_class, serializer_class):
        return 'a'
        # TODO
        qs = model_class.objects.filter(student_detailed_info__id=obj.id)
        return serializer_class(qs, many=True, context=self.context).data


class StudentDetailedInfoSerializer(StudentDetailedInfoBaseSerializer):
    from abroadin.apps.users.customAuth.serializers import SafeUserDataSerializer

    user = SafeUserDataSerializer(read_only=True)
    want_to_applies = serializers.SerializerMethodField()

    class Meta(StudentDetailedInfoBaseSerializer.Meta):
        model = StudentDetailedInfo
        fields = StudentDetailedInfoBaseSerializer.Meta.fields + [
            'user', 'age', 'gender', 'is_married',
            'want_to_applies', 'payment_affordability',
            'prefers_full_fund', 'prefers_half_fund', 'prefers_self_fund',
            'comment', 'powerful_recommendation', 'linkedin_url', 'homepage_url',
        ]

    def get_want_to_applies(self, obj):
        qs = WantToApply.objects.filter(student_detailed_info__id=obj.id)
        return WantToApplySerializer(qs, many=True, context=self.context).data


class StudentDetailedInfoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user',
            'age', 'is_married',
            'payment_affordability', 'gender',
            'prefers_full_fund', 'prefers_half_fund', 'prefers_self_fund',
            'comment', 'resume', 'related_work_experience', 'academic_break', 'olympiad', 'powerful_recommendation',
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
