from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from abroadin.apps.data.account.models import BasicFormField, University, Major
from abroadin.apps.data.account.serializers import CountrySerializer, UniversitySerializer, MajorSerializer

from .models import (
    SemesterYear, Publication, Grade, Education, Admission, LanguageCertificate,
    RegularLanguageCertificate, GMATCertificate, GREGeneralCertificate, GRESubjectCertificate, GREPhysicsCertificate,
    GREBiologyCertificate, GREPsychologyCertificate, DuolingoCertificate)

from abroadin.apps.estimation.form.models import StudentDetailedInfo

from abroadin.apps.platform.applyProfile.models import ApplyProfile

LanguageCertificateType = LanguageCertificate.LanguageCertificateType


class ContentTypeRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return ContentType.objects.filter(app_label='storePackages', model='soldstorepaidpackagephase') | \
               ContentType.objects.filter(app_label='storePackages', model='soldstoreunpaidpackagephase')

    def to_internal_value(self, data):
        print('TOOOINTERNALVALUEEEEEEEEEEEEEEE')
        if data == 'soldstorepaidpackagephase':
            return ContentType.objects.get(app_label='storePackages', model='soldstorepaidpackagephase')
        elif data == 'soldstoreunpaidpackagephase':
            return ContentType.objects.get(app_label='storePackages', model='soldstoreunpaidpackagephase')
        else:
            raise serializers.ValidationError({"content_type": "ContentTypeRelatedField wrong instance."}, code=400)

    def to_representation(self, value):
        print('ASDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
        print(value)
        if isinstance(value, ApplyProfile):
            print('is apply profile')
            return {'model': 'ApplyProfile', 'object_id': value.id}
        elif value.model_class() == StudentDetailedInfo:
            return 'soldstoreunpaidpackagephase'
        else:
            raise serializers.ValidationError({"content_type": "ContentTypeRelatedField wrong instance."}, code=400)


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ["id", "name"]


class SemesterYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterYear
        fields = ['id', 'year', 'semester']


class SemesterYearCustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
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
        obj = SemesterYear.objects.get(pk=value.pk)
        return SemesterYearSerializer(obj).data


class BasicFormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicFormField
        fields = ['id', 'name']


class PublicationSerializer(serializers.ModelSerializer):
    content_object = ContentTypeRelatedField(
        read_only=True,
    )

    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'publish_year', 'which_author', 'type', 'journal_reputation',
            'content_object',
        ]

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class PublicationRequestSerializer(serializers.ModelSerializer):
    # student_detailed_info = serializers.PrimaryKeyRelatedField(
    #     queryset=abroadin.apps.estimation.form.models.StudentDetailedInfo.objects.all(),
    #     pk_field=serializers.UUIDField(label='id'),
    #     allow_null=False,
    #     allow_empty=False,
    #     required=True,
    # )

    content_object = ContentTypeRelatedField(
        read_only=True
    )

    class Meta:
        model = Publication
        fields = [
            'id', 'content_object', 'title', 'publish_year', 'which_author', 'type', 'journal_reputation',
        ]

    # def validate(self, attrs):
    #     request = self.context.get("request")
    #     if request and hasattr(request, "user"):
    #         request_user = request.user
    #         student_detailed_info = attrs.get("student_detailed_info")
    #         if student_detailed_info.user is not None and student_detailed_info.user != request_user:
    #             raise ValidationError(_("User can't set student_detailed_info of another user."))
    #         if student_detailed_info.user is None and request_user.is_authenticated:
    #             raise ValidationError(_("User can't set student_detailed_info of another user."))
    #     else:
    #         raise ValidationError(_("Can't validate data.Can't get request user."))
    #     return attrs


class EducationSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()
    major = MajorSerializer()

    class Meta:
        model = Education
        fields = [
            'id', 'university', 'content_object', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
        ]

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class EducationRequestSerializer(serializers.ModelSerializer):
    university = serializers.PrimaryKeyRelatedField(
        queryset=University.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )

    # student_detailed_info = serializers.PrimaryKeyRelatedField(
    #     queryset=StudentDetailedInfo.objects.all(),
    #     pk_field=serializers.UUIDField(label='id'),
    #     allow_null=False,
    #     allow_empty=False,
    #     required=True,
    # )
    major = serializers.PrimaryKeyRelatedField(
        queryset=Major.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )

    class Meta:
        model = Education
        fields = [
            'id', 'university', 'content_object', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
        ]

    # def validate(self, attrs):
    #     request = self.context.get("request")
    #     if request and hasattr(request, "user"):
    #         request_user = request.user
    #         student_detailed_info = attrs.get("student_detailed_info")
    #         if student_detailed_info.user is not None and student_detailed_info.user != request_user:
    #             raise ValidationError(_("User can't set student_detailed_info of another user."))
    #         if student_detailed_info.user is None and request_user.is_authenticated:
    #             raise ValidationError(_("User can't set student_detailed_info of another user."))
    #     else:
    #         raise ValidationError(_("Can't validate data.Can't get request user."))
    #     return attrs


class LanguageCertificateSerializer(serializers.ModelSerializer):
    # student_detailed_info = serializers.PrimaryKeyRelatedField(
    #     queryset=abroadin.apps.estimation.form.models.StudentDetailedInfo.objects.all(),
    #     pk_field=serializers.UUIDField(label='id'),
    #     allow_null=False,
    #     allow_empty=False,
    #     required=True,
    # )

    class Meta:
        model = LanguageCertificate
        fields = '__all__'

    # def validate(self, attrs):
    #     request = self.context.get("request")
    #     if request and hasattr(request, "user"):
    #         request_user = request.user
    #         student_detailed_info = attrs.get("student_detailed_info")
    #         if student_detailed_info.user is not None and student_detailed_info.user != request_user:
    #             raise ValidationError(
    #                 {'student_detailed_info': _("User can't set student_detailed_info of another user.")})
    #         if student_detailed_info.user is None and request_user.is_authenticated:
    #             raise ValidationError(
    #                 {'student_detailed_info': _("User can't set student_detailed_info of another user.")})
    #     else:
    #         raise ValidationError(_("Can't validate data.Can't get request user."))
    #     return attrs


class RegularLanguageCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = RegularLanguageCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.IELTS_ACADEMIC, LanguageCertificateType.IELTS_GENERAL,
                         LanguageCertificateType.TOEFL]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class RegularLanguageCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularLanguageCertificate
        validators = []
        exclude = ['content_object']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GMATCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GMATCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GMAT]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GMATCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GMATCertificate
        validators = []
        exclude = ['content_object']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GREGeneralCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GREGeneralCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GRE_GENERAL]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREGeneralCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GREGeneralCertificate
        validators = []
        exclude = ['content_object']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GRESubjectCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GRESubjectCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GRE_CHEMISTRY, LanguageCertificateType.GRE_LITERATURE,
                         LanguageCertificateType.GRE_MATHEMATICS]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GRESubjectCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GRESubjectCertificate
        validators = []
        exclude = ['content_object']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GREBiologyCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GREBiologyCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GRE_BIOLOGY]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREPhysicsCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GREPhysicsCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GRE_PHYSICS]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREPsychologyCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GREPsychologyCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.GRE_PSYCHOLOGY]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class DuolingoCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = DuolingoCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LanguageCertificateType.DUOLINGO]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class DuolingoCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = DuolingoCertificate
        validators = []
        exclude = ['content_object']

    default_validators = []

    def validate(self, attrs):
        return attrs


class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = [
            'id', 'enrolled', 'origin_university', 'goal_university',
            'scholarships', 'scholarships_unit', 'major',
            'academic_gap', 'accepted', 'description', 'choose_reason',
        ]