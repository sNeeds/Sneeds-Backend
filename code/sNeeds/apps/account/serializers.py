from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError
from . import models
from .models import StudentDetailedInfo, StudentFormApplySemesterYear, BasicFormField, University,\
    WantToApply, Publication, UniversityThrough, GRECertificate, GMATCertificate

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
    university = UniversitySerializer()
    grade = BasicFormFieldSerializer()
    major = BasicFormFieldSerializer()
    semester_year = StudentFormApplySemesterYearSerializer()

    class Meta:
        model = models.WantToApply
        fields = [
            'id', 'student_detailed_info', 'country', 'university', 'grade', 'major', 'semester_year',
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
    university = serializers.PrimaryKeyRelatedField(
        queryset=models.University.objects.all(),
        pk_field=serializers.IntegerField(label='id'),
        allow_null=True,
        allow_empty=True,
        required=False,
    )
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
            'id', 'student_detailed_info', 'country', 'university',
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
    which_author = BasicFormFieldSerializer()
    type = BasicFormFieldSerializer()

    class Meta:
        model = models.Publication
        fields = [
            'id', 'student_detailed_info', 'title', 'publish_year', 'which_author', 'type',
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

    class Meta:
        model = models.Publication
        fields = [
            'id', 'student_detailed_info', 'title', 'publish_year', 'which_author', 'type',
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
    university = BasicFormFieldSerializer()
    grade = BasicFormFieldSerializer()
    major = BasicFormFieldSerializer()

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


# class LanguageCertificateTypeThroughSerializer(serializers.ModelSerializer):
#     certificate_type = BasicFormFieldSerializer()
#
#     class Meta:
#         model = models.LanguageCertificateTypeThrough
#         fields = [
#             'id', 'certificate_type', 'student_detailed_info',
#             'speaking', 'listening', 'writing', 'reading', 'overall',
#         ]
#
#     def create(self, validated_data):
#         raise ValidationError(_("Creating object through this serializer is not allowed"))


# class LanguageCertificateTypeThroughRequestSerializer(serializers.ModelSerializer):
#     certificate_type = serializers.PrimaryKeyRelatedField(
#         queryset=models.LanguageCertificateType.objects.all(),
#         pk_field=serializers.IntegerField(label='id'),
#         allow_null=False,
#         allow_empty=False,
#         required=True,
#     )
#
#     student_detailed_info = serializers.PrimaryKeyRelatedField(
#         queryset=models.StudentDetailedInfo.objects.all(),
#         pk_field=serializers.IntegerField(label='id'),
#         allow_null=False,
#         allow_empty=False,
#         required=True,
#     )
#
#     class Meta:
#         model = models.LanguageCertificateTypeThrough
#         fields = [
#             'id', 'certificate_type', 'student_detailed_info',
#             'speaking', 'listening', 'writing', 'reading', 'overall',
#         ]
#
#     def validate(self, attrs):
#         request_user = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             request_user = request.user
#             student_detailed_info = attrs.get("student_detailed_info")
#             if student_detailed_info.user is not None and student_detailed_info.user != request_user:
#                 raise ValidationError(_("User can't set student_detailed_info of another user."))
#             if student_detailed_info.user is None and request_user.is_authenticated:
#                 raise ValidationError(_("User can't set student_detailed_info of another user."))
#         else:
#             raise ValidationError(_("Can't validate data.Can't get request user."))
#         return attrs


class GMATCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GMATCertificate
        fields = [
            'id', 'student_detailed_info', 'analytical_writing_assessment', 'integrated_reasoning',
            'quantitative_and_verbal', 'total'
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


class GRECertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GRECertificate
        fields = [
            'id', 'student_detailed_info', 'quantitative', 'verbal', 'analytical_writing',
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


class StudentDetailedInfoSerializer(serializers.ModelSerializer):
    from sNeeds.apps.customAuth.serializers import SafeUserDataSerializer
    user = SafeUserDataSerializer(read_only=True)

    gre_certificate = serializers.SerializerMethodField()
    gmat_certificate = serializers.SerializerMethodField()

    is_married = BasicFormFieldSerializer()
    payment_affordability = BasicFormFieldSerializer()

    universities = serializers.SerializerMethodField()
    # language_certificates = serializers.SerializerMethodField()
    want_to_applies = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()

    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user',
            'age', 'is_married',
            'universities', 'want_to_applies', 'publications',
            'language_certificates', 'gre_certificate', 'gmat_certificate',
            'payment_affordability', 'prefers_full_fund', 'prefers_half_fund', 'prefers_self_fund',
            'comment', 'resume', 'related_work_experience', 'academic_break', 'olympiad', 'powerful_recommendation',
            'linkedin_url', 'homepage_url',
            'created', 'updated',
        ]

    def get_gre_certificate(self, obj):
        qs = GRECertificate.objects.filter(student_detailed_info=obj)
        return GRECertificateSerializer(qs, many=True, context=self.context).data

    def get_gmat_certificate(self, obj):
        qs = GMATCertificate.objects.filter(student_detailed_info=obj)
        return GMATCertificateSerializer(qs, many=True, context=self.context).data

    def get_universities(self, obj):
        qs = UniversityThrough.objects.filter(student_detailed_info_id=obj.id)
        return UniversityThroughSerializer(qs, many=True, context=self.context).data

    # def get_language_certificates(self, obj):
    #     qs = LanguageCertificateTypeThrough.objects.filter(student_detailed_info_id=obj.id)
    #     return LanguageCertificateTypeThroughSerializer(qs, many=True, context=self.context).data

    def get_want_to_applies(self, obj):
        qs = WantToApply.objects.filter(student_detailed_info_id=obj.id)
        return WantToApplySerializer(qs, many=True, context=self.context).data

    def get_publications(self, obj):
        qs = Publication.objects.filter(student_detailed_info_id=obj.id)
        return PublicationSerializer(qs, many=True, context=True).data

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class StudentDetailedInfoRequestSerializer(serializers.ModelSerializer):
    # payment_affordability = serializers.PrimaryKeyRelatedField(
    #     queryset=models.PaymentAffordability.objects.all(),
    #     pk_field=serializers.IntegerField(label='id'),
    #     allow_null=True,
    #     allow_empty=True,
    #     required=False,
    # )

    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user',
            'age', 'is_married',
            'payment_affordability', 'prefers_full_fund', 'prefers_half_fund', 'prefers_self_fund',
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
