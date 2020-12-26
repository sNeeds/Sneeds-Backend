from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from abroadin.apps.data.account.models import BasicFormField, University, Major
from abroadin.apps.data.account.serializers import CountrySerializer, UniversitySerializer, MajorSerializer
from abroadin.base.api.fields import GenericRelatedField, ContentTypeRelatedField, GenericHyperlinkedRelatedField
from abroadin.base.api.serializers import generic_hyperlinked_related_method

from .models import (
    SemesterYear, Publication, Grade, Education, Admission, LanguageCertificate,
    RegularLanguageCertificate, GMATCertificate, GREGeneralCertificate, GRESubjectCertificate, GREPhysicsCertificate,
    GREBiologyCertificate, GREPsychologyCertificate, DuolingoCertificate)

from abroadin.apps.estimation.form.models import StudentDetailedInfo

from abroadin.apps.platform.applyProfile.models import ApplyProfile

LanguageCertificateType = LanguageCertificate.LanguageCertificateType


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
    related_classes = [
        {
            'model_class': ApplyProfile,
            'hyperlink_view_name': 'platform.applyProfile:apply-profile-detail',
            'hyperlink_lookup_field': 'id',
            'hyperlink_lookup_url_kwarg': 'id',
            'hyperlink_format': None
        },
        {
            'model_class': StudentDetailedInfo,
            'hyperlink_view_name': 'estimation.form:student-detailed-info-detail',
            'hyperlink_lookup_field': 'id',
            'hyperlink_lookup_url_kwarg': 'form-id',
            'hyperlink_format': None
        }
    ]

    content_type = ContentTypeRelatedField(
        related_classes=related_classes,
    )

    # content_object = GenericRelatedField(
    #     related_classes=[
    #         {
    #             'model_class': ApplyProfile,
    #             # 'representation_identifier': '',
    #             'primary_key_related_field': serializers.PrimaryKeyRelatedField(
    #                 queryset=ApplyProfile.objects.all()
    #             ),
    #             'hyperlinked_related_field': serializers.HyperlinkedRelatedField(
    #                 queryset=ApplyProfile.objects.all(),
    #                 lookup_field='id',
    #                 view_name='platform.applyProfile:apply-profile-list'
    #             ),
    #         }
    #     ]
    # )

    content_url = SerializerMethodField(method_name='get_content_url')

    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'publish_year', 'which_author', 'type', 'journal_reputation',
            'content_type', 'object_id',
            # 'content_object',
            'content_url',
        ]

        extra_kwargs = {
            # 'content_object': {'read_only': True},
        }

    def get_content_url(self, obj):
        return generic_hyperlinked_related_method(self, self.related_classes, obj)


class PublicationRequestSerializer(serializers.ModelSerializer):
    related_classes = [
        {
            'model_class': ApplyProfile,
            'hyperlink_view_name': 'platform.applyProfile:apply-profile-detail',
            'hyperlink_lookup_field': 'id',
            'hyperlink_lookup_url_kwarg': 'id',
            'hyperlink_format': None
        }
    ]

    content_type = ContentTypeRelatedField(
        related_classes=related_classes,
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

    related_classes = [
        {
            'model_class': ApplyProfile,
            'hyperlink_view_name': 'platform.applyProfile:apply-profile-detail',
            'hyperlink_lookup_field': 'id',
            'hyperlink_lookup_url_kwarg': 'id',
            # 'hyperlink_format': None
        }
    ]

    content_type = ContentTypeRelatedField(
        related_classes=related_classes,
    )

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

    major = serializers.PrimaryKeyRelatedField(
        queryset=Major.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )

    related_classes = [
        {
            'model_class': ApplyProfile,
            'hyperlink_view_name': 'platform.applyProfile:apply-profile-detail',
            'hyperlink_lookup_field': 'id',
            'hyperlink_lookup_url_kwarg': 'id',
            # 'hyperlink_format': None
        }
    ]

    content_type = ContentTypeRelatedField(
        related_classes=related_classes,
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
    related_classes = [
        {
            'model_class': ApplyProfile,
            'hyperlink_view_name': 'platform.applyProfile:apply-profile-detail',
            'hyperlink_lookup_field': 'id',
            'hyperlink_lookup_url_kwarg': 'id',
            # 'hyperlink_format': None
        }
    ]

    content_type = ContentTypeRelatedField(
        related_classes=related_classes,
    )

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
    related_classes = [
        {
            'model_class': ApplyProfile,
            'hyperlink_view_name': 'platform.applyProfile:apply-profile-detail',
            'hyperlink_lookup_field': 'id',
            'hyperlink_lookup_url_kwarg': 'id',
            'hyperlink_format': None
        }
    ]

    content_type = ContentTypeRelatedField(
        related_classes=related_classes,
    )

    class Meta:
        model = Admission
        fields = [
            'id', 'enrolled', 'origin_university', 'goal_university',
            'scholarships', 'scholarships_unit', 'major',
            'academic_gap', 'accepted', 'description', 'choose_reason',
        ]
