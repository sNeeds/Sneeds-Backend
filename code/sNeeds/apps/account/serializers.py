from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError
from . import fields

from . import models
from . import validators
from .models import StudentDetailedInfo, StudentFormApplySemesterYear, BasicFormField, University, \
    WantToApply, Publication, UniversityThrough, LanguageCertificateType, Grade, WhichAuthor

User = get_user_model()


# TODO: Move SoldTimeSlotRate

class CountrySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:country-detail",
        lookup_field='slug',
        read_only=True
    )

    class Meta:
        model = models.Country
        fields = ('id', 'url', 'name', 'slug', 'picture')


class UniversitySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:university-detail",
        lookup_field='id',
        read_only=True
    )
    country = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="account:country-detail",
        lookup_field='slug',
    )

    class Meta:
        model = models.University
        fields = ('id', 'url', 'name', 'country', 'description', 'picture')


class FieldOfStudySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:field-of-study-detail",
        lookup_field='id',
        read_only=True
    )

    class Meta:
        model = models.FieldOfStudy
        fields = ('id', 'url', 'name', 'description', 'picture')


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
    country = CountrySerializer()
    universities = UniversitySerializer(many=True)
    grade = fields.EnumField(enum=Grade)
    major = FieldOfStudySerializer()
    semester_year = StudentFormApplySemesterYearSerializer()

    class Meta:
        model = models.WantToApply
        fields = [
            'id', 'student_detailed_info', 'country', 'universities', 'grade', 'major', 'semester_year',
        ]

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class WantToApplyRequestSerializer(serializers.ModelSerializer):
    student_detailed_info = serializers.PrimaryKeyRelatedField(
        queryset=models.StudentDetailedInfo.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )
    country = serializers.PrimaryKeyRelatedField(
        queryset=models.Country.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )
    universities = serializers.PrimaryKeyRelatedField(
        queryset=models.University.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=True,
        allow_empty=True,
        required=False,
    )

    grade = fields.EnumField(enum=Grade)

    major = serializers.PrimaryKeyRelatedField(
        queryset=models.FieldOfStudy.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=True,
        allow_empty=True,
        required=False,
    )
    semester_year = serializers.PrimaryKeyRelatedField(
        queryset=models.StudentFormApplySemesterYear.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )

    class Meta:
        model = models.WantToApply
        fields = [
            'id', 'student_detailed_info', 'country', 'universities',
            'grade', 'major',
            'semester_year',
        ]

    def validate(self, attrs):
        request_user = None
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
    which_author = fields.EnumField(enum=models.WhichAuthor)
    type = fields.EnumField(enum=models.PublicationType)
    journal_reputation = fields.EnumField(enum=models.JournalReputation)

    class Meta:
        model = models.Publication
        fields = [
            'id', 'student_detailed_info', 'title', 'publish_year', 'which_author', 'type', 'journal_reputation',
        ]

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class PublicationRequestSerializer(serializers.ModelSerializer):
    student_detailed_info = serializers.PrimaryKeyRelatedField(
        queryset=models.StudentDetailedInfo.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )

    which_author = fields.EnumField(enum=models.WhichAuthor)
    type = fields.EnumField(enum=models.PublicationType)
    journal_reputation = fields.EnumField(enum=models.JournalReputation)

    class Meta:
        model = models.Publication
        fields = [
            'id', 'student_detailed_info', 'title', 'publish_year', 'which_author', 'type', 'journal_reputation',
        ]

    def validate(self, attrs):
        request_user = None
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
    grade = fields.EnumField(enum=models.Grade)
    major = FieldOfStudySerializer()

    class Meta:
        model = models.UniversityThrough
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
        queryset=models.StudentDetailedInfo.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )
    major = serializers.PrimaryKeyRelatedField(
        queryset=models.FieldOfStudy.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )

    grade = fields.EnumField(enum=models.Grade)

    class Meta:
        model = models.UniversityThrough
        fields = [
            'id', 'university', 'student_detailed_info', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
        ]

    def validate(self, attrs):
        request_user = None
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
        queryset=models.StudentDetailedInfo.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=False,
        allow_empty=False,
        required=True,
    )

    certificate_type = fields.EnumField(enum=LanguageCertificateType)

    class Meta:
        model = models.LanguageCertificate
        fields = '__all__'

    def validate(self, attrs):
        request_user = None
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
        model = models.RegularLanguageCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        certificate_types = models.LanguageCertificateType
        if value not in [certificate_types.IELTS, certificate_types.TOEFL]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GMATCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = models.GMATCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        certificate_types = models.LanguageCertificateType
        if value not in [certificate_types.GMAT]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREGeneralCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = models.GREGeneralCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        certificate_types = models.LanguageCertificateType
        if value not in [certificate_types.GRE_GENERAL]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GRESubjectCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = models.GRESubjectCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        certificate_types = models.LanguageCertificateType
        if value not in [certificate_types.GRE_CHEMISTRY, certificate_types.GRE_LITERATURE,
                         certificate_types.GRE_MATHEMATICS]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREBiologyCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = models.GREBiologyCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        certificate_types = models.LanguageCertificateType
        if value not in [certificate_types.GRE_BIOLOGY]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREPhysicsCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = models.GREPhysicsCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        certificate_types = models.LanguageCertificateType
        if value not in [certificate_types.GRE_PHYSICS]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREPsychologyCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = models.GREPsychologyCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        certificate_types = models.LanguageCertificateType
        if value not in [certificate_types.GRE_PSYCHOLOGY]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class DuolingoCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = models.DuolingoCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        certificate_types = models.LanguageCertificateType
        if value not in [certificate_types.DUOLINGO]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class StudentDetailedInfoSerializer(serializers.ModelSerializer):
    from sNeeds.apps.customAuth.serializers import SafeUserDataSerializer
    user = SafeUserDataSerializer(read_only=True)

    regular_certificates = serializers.SerializerMethodField()
    gmat_certificates = serializers.SerializerMethodField()
    gre_general_certificates = serializers.SerializerMethodField()
    gre_subject_certificates = serializers.SerializerMethodField()
    gre_biology_certificates = serializers.SerializerMethodField()
    gre_physics_certificates = serializers.SerializerMethodField()
    gre_psychology_certificates = serializers.SerializerMethodField()
    duolingo_certificates = serializers.SerializerMethodField()

    universities = serializers.SerializerMethodField()
    want_to_applies = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()

    payment_affordability = fields.EnumField(enum=models.PaymentAffordability)
    gender = fields.EnumField(enum=models.Gender)
    military_service_status = fields.EnumField(enum=models.MilitaryServiceStatus)

    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user',
            'age', 'is_married',
            'universities', 'want_to_applies', 'publications',
            'payment_affordability', 'gender', 'military_service_status',
            'regular_certificates', 'gmat_certificates', 'gre_general_certificates', 'gre_subject_certificates',
            'gre_biology_certificates', 'gre_physics_certificates', 'gre_psychology_certificates',
            'duolingo_certificates',
            'prefers_full_fund', 'prefers_half_fund', 'prefers_self_fund',
            'comment', 'resume', 'related_work_experience', 'academic_break', 'olympiad', 'powerful_recommendation',
            'linkedin_url', 'homepage_url',
            'created', 'updated',
        ]

    def get_regular_certificates(self, obj):
        return self.certificates(obj, models.RegularLanguageCertificate, RegularLanguageCertificateSerializer)

    def get_gmat_certificates(self, obj):
        return self.certificates(obj, models.GMATCertificate, GMATCertificateSerializer)

    def get_gre_general_certificates(self, obj):
        return self.certificates(obj, models.GREGeneralCertificate, GREGeneralCertificateSerializer)

    def get_gre_subject_certificates(self, obj):
        return self.certificates(obj, models.GRESubjectCertificate, GRESubjectCertificateSerializer)

    def get_gre_biology_certificates(self, obj):
        return self.certificates(obj, models.GREBiologyCertificate, GREBiologyCertificateSerializer)

    def get_gre_physics_certificates(self, obj):
        return self.certificates(obj, models.GREPhysicsCertificate, GREPhysicsCertificateSerializer)

    def get_gre_psychology_certificates(self, obj):
        return self.certificates(obj, models.GREPsychologyCertificate, GREPsychologyCertificateSerializer)

    def get_duolingo_certificates(self, obj):
        return self.certificates(obj, models.DuolingoCertificate, DuolingoCertificateSerializer)

    def get_universities(self, obj):
        qs = UniversityThrough.objects.filter(student_detailed_info_id=obj.id)
        return UniversityThroughSerializer(qs, many=True, context=self.context).data

    def get_want_to_applies(self, obj):
        qs = WantToApply.objects.filter(student_detailed_info_id=obj.id)
        return WantToApplySerializer(qs, many=True, context=self.context).data

    def get_publications(self, obj):
        qs = Publication.objects.filter(student_detailed_info_id=obj.id)
        return PublicationSerializer(qs, many=True, context=True).data

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))

    # Custom method
    def certificates(self, obj, model_class, serializer_class):
        qs = model_class.objects.filter(student_detailed_info_id=obj.id)
        return serializer_class(qs, many=True, context=self.context).data


class StudentDetailedInfoRequestSerializer(serializers.ModelSerializer):
    payment_affordability = fields.EnumField(enum=models.PaymentAffordability, required=False)
    gender = fields.EnumField(enum=models.Gender, required=False)
    military_service_status = fields.EnumField(enum=models.MilitaryServiceStatus, required=False)

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
        request = self.context.get('request')
        request_user = request.user
        data_user = attrs.get("user")
        if data_user is not None:
            if data_user != request_user:
                raise ValidationError(_("User can't set another user as the user of object."))
            if data_user.is_consultant():
                raise ValidationError(_("Consultants can not have Student Detailed Info"))
            if data_user.is_authenticated:
                user_student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=data_user)
                if user_student_detailed_info_qs.exists():
                    raise ValidationError(_("User already has a student detailed info"))
        return attrs

    def create(self, validated_data):
        data_user = validated_data.get("user")
        if data_user is not None:
            user_student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=data_user)
            if user_student_detailed_info_qs.exists():
                raise ValidationError(_("User already has a student detailed info"))
        student_detailed_info_obj = StudentDetailedInfo.objects.create(**validated_data)
        return student_detailed_info_obj
