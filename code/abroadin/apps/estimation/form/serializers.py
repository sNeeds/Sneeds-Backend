from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import abroadin.apps
import abroadin.apps.estimation.form.models
from abroadin.apps.estimation.form.models import StudentFormApplySemesterYear, WantToApply, StudentDetailedInfo, \
    UniversityThrough, Publication
from abroadin.apps.data.account import models
from abroadin.apps.data.account.models import BasicFormField
from abroadin.apps.data.account.serializers import CountrySerializer, UniversitySerializer, MajorSerializer

LanguageCertificateType = abroadin.apps.estimation.form.models.LanguageCertificate.LanguageCertificateType


class StudentFormApplySemesterYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFormApplySemesterYear
        fields = ['id', 'year', 'semester']


class StudentFormApplySemesterYearCustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_choices(self, cutoff=None):
        """
        This method is overridden.
        Issue was:
        https://stackoverflow.com/questions/50973569/django-rest-framework-relatedfield-cant-return-a-dict-object
        """
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])

    def to_representation(self, value):
        obj = StudentFormApplySemesterYear.objects.get(pk=value.pk)
        return StudentFormApplySemesterYearSerializer(obj).data


class BasicFormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicFormField
        fields = ['id', 'name']


class WantToApplySerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True)
    universities = UniversitySerializer(many=True)
    majors = MajorSerializer(many=True)
    semester_years = StudentFormApplySemesterYearSerializer(many=True)

    class Meta:
        model = abroadin.apps.estimation.form.models.WantToApply
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
        queryset=abroadin.apps.estimation.form.models.StudentFormApplySemesterYear.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
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
        sdi_want_to_applies_qs = WantToApply.objects.filter(student_detailed_info=student_detailed_info)
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


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.Publication
        fields = [
            'id', 'student_detailed_info', 'title', 'publish_year', 'which_author', 'type', 'journal_reputation',
        ]

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class PublicationRequestSerializer(serializers.ModelSerializer):
    student_detailed_info = serializers.PrimaryKeyRelatedField(
        queryset=abroadin.apps.estimation.form.models.StudentDetailedInfo.objects.all(),
        pk_field=serializers.UUIDField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )

    class Meta:
        model = abroadin.apps.estimation.form.models.Publication
        fields = [
            'id', 'student_detailed_info', 'title', 'publish_year', 'which_author', 'type', 'journal_reputation',
        ]

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


class UniversityThroughSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()
    major = MajorSerializer()

    class Meta:
        model = abroadin.apps.estimation.form.models.UniversityThrough
        fields = [
            'id', 'university', 'student_detailed_info', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
        ]

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class UniversityThroughRequestSerializer(serializers.ModelSerializer):
    university = serializers.PrimaryKeyRelatedField(
        queryset=models.University.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )

    student_detailed_info = serializers.PrimaryKeyRelatedField(
        queryset=abroadin.apps.estimation.form.models.StudentDetailedInfo.objects.all(),
        pk_field=serializers.UUIDField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )
    major = serializers.PrimaryKeyRelatedField(
        queryset=models.Major.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )

    class Meta:
        model = abroadin.apps.estimation.form.models.UniversityThrough
        fields = [
            'id', 'university', 'student_detailed_info', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
        ]

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


class LanguageCertificateSerializer(serializers.ModelSerializer):
    student_detailed_info = serializers.PrimaryKeyRelatedField(
        queryset=abroadin.apps.estimation.form.models.StudentDetailedInfo.objects.all(),
        pk_field=serializers.UUIDField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )

    class Meta:
        model = abroadin.apps.estimation.form.models.LanguageCertificate
        fields = '__all__'

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
        return attrs


class RegularLanguageCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.RegularLanguageCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.IELTS_ACADEMIC, LanguageCertificateType.IELTS_GENERAL,
                         LanguageCertificateType.TOEFL]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class RegularLanguageCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.RegularLanguageCertificate
        validators = []
        exclude = ['student_detailed_info']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GMATCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.GMATCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GMAT]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GMATCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.GMATCertificate
        validators = []
        exclude = ['student_detailed_info']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GREGeneralCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.GREGeneralCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GRE_GENERAL]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREGeneralCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.GREGeneralCertificate
        validators = []
        exclude = ['student_detailed_info']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GRESubjectCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.GRESubjectCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GRE_CHEMISTRY, LanguageCertificateType.GRE_LITERATURE,
                         LanguageCertificateType.GRE_MATHEMATICS]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GRESubjectCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.GRESubjectCertificate
        validators = []
        exclude = ['student_detailed_info']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GREBiologyCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.GREBiologyCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GRE_BIOLOGY]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREPhysicsCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.GREPhysicsCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GRE_PHYSICS]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREPsychologyCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.GREPsychologyCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GRE_PSYCHOLOGY]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class DuolingoCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.DuolingoCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.DUOLINGO]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class DuolingoCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = abroadin.apps.estimation.form.models.DuolingoCertificate
        validators = []
        exclude = ['student_detailed_info']

    default_validators = []

    def validate(self, attrs):
        return attrs


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
        return self.get_certificates(obj, abroadin.apps.estimation.form.models.RegularLanguageCertificate,
                                     RegularLanguageCertificateSerializer)

    def get_gmat_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.estimation.form.models.GMATCertificate,
                                     GMATCertificateSerializer)

    def get_gre_general_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.estimation.form.models.GREGeneralCertificate,
                                     GREGeneralCertificateSerializer)

    def get_gre_subject_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.estimation.form.models.GRESubjectCertificate,
                                     GRESubjectCertificateSerializer)

    def get_gre_biology_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.estimation.form.models.GREBiologyCertificate,
                                     GREBiologyCertificateSerializer)

    def get_gre_physics_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.estimation.form.models.GREPhysicsCertificate,
                                     GREPhysicsCertificateSerializer)

    def get_gre_psychology_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.estimation.form.models.GREPsychologyCertificate,
                                     GREPsychologyCertificateSerializer)

    def get_duolingo_certificates(self, obj):
        return self.get_certificates(obj, abroadin.apps.estimation.form.models.DuolingoCertificate,
                                     DuolingoCertificateSerializer)

    def get_universities(self, obj):
        qs = UniversityThrough.objects.filter(student_detailed_info_id=obj.id)
        return UniversityThroughSerializer(qs, many=True, context=self.context).data

    def get_publications(self, obj):
        qs = Publication.objects.filter(student_detailed_info__id=obj.id)
        return PublicationSerializer(qs, many=True, context=True).data

    def create(self, validated_data):
        raise ValidationError(_("Create object through this serializer is not allowed"))

    def update(self, instance, validated_data):
        raise ValidationError(_("Update object through this serializer is not allowed"))

    # Custom method
    def get_certificates(self, obj, model_class, serializer_class):
        qs = model_class.objects.filter(student_detailed_info_id=obj.id)
        return serializer_class(qs, many=True, context=self.context).data


class StudentDetailedInfoSerializer(StudentDetailedInfoBaseSerializer):
    from abroadin.apps.users.customAuth.serializers import SafeUserDataSerializer

    user = SafeUserDataSerializer(read_only=True)
    want_to_applies = serializers.SerializerMethodField()

    class Meta(StudentDetailedInfoBaseSerializer.Meta):
        model = StudentDetailedInfo
        fields = StudentDetailedInfoBaseSerializer.Meta.fields + [
            'user', 'age', 'gender', 'military_service_status', 'is_married',
            'want_to_applies', 'payment_affordability',
            'prefers_full_fund', 'prefers_half_fund', 'prefers_self_fund',
            'comment', 'powerful_recommendation', 'linkedin_url', 'homepage_url',
        ]

    def get_want_to_applies(self, obj):
        qs = WantToApply.objects.filter(student_detailed_info_id=obj.id)
        return WantToApplySerializer(qs, many=True, context=self.context).data


class StudentDetailedInfoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user',
            'age', 'is_married',
            'payment_affordability', 'gender', 'military_service_status',
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
