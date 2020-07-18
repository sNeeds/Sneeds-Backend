from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError
from . import models
from .models import StudentDetailedInfo, StudentFormApplySemesterYear, BasicFormField, FormUniversityThrough, \
    LanguageCertificateTypeThrough, WantToApply, Publication

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
    url = serializers.HyperlinkedIdentityField(view_name="account:university-detail", lookup_field='slug',
                                               read_only=True)
    country = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="account:country-detail",
        lookup_field='slug',
    )

    class Meta:
        model = models.University
        fields = ('id', 'url', 'name', 'country', 'description', 'slug', 'picture')


class FieldOfStudySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:field-of-study-detail",
        lookup_field='slug',
        read_only=True
    )

    class Meta:
        model = models.FieldOfStudy
        fields = ('id', 'url', 'name', 'description', 'slug', 'picture')


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
            'id', 'form', 'country', 'university', 'grade', 'major', 'semester_year',
        ]


class WantToApplyRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WantToApply
        fields = [
            'id', 'form', 'country', 'university', 'grade', 'major', 'semester_year',
        ]


class PublicationSerializer(serializers.ModelSerializer):
    which_author = BasicFormFieldSerializer()
    type = BasicFormFieldSerializer()

    class Meta:
        model = models.Publication
        fields = [
            'id', 'student_detailed_info', 'title', 'publish_year', 'which_author', 'type',
        ]


class PublicationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publication
        fields = [
            'id', 'student_detailed_info', 'title', 'publish_year', 'which_author', 'type',
        ]


class FormUniversityThroughSerializer(serializers.ModelSerializer):
    university = BasicFormFieldSerializer()
    grade = BasicFormFieldSerializer()
    major = BasicFormFieldSerializer()

    class Meta:
        model = models.FormUniversityThrough
        fields = [
            'id', 'university', 'student_detailed_info', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
        ]


class FormUniversityThroughRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormUniversityThrough
        fields = [
            'id', 'university', 'student_detailed_info', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
        ]


class LanguageCertificateTypeThroughSerializer(serializers.ModelSerializer):
    certificate_type = BasicFormFieldSerializer()

    class Meta:
        model = models.LanguageCertificateTypeThrough
        fields = [
            'id', 'certificate_type', 'student_detailed_info',
            'speaking', 'listening', 'writing', 'reading', 'overall',
        ]


class LanguageCertificateTypeThroughRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LanguageCertificateTypeThrough
        fields = [
            'id', 'certificate_type', 'student_detailed_info',
            'speaking', 'listening', 'writing', 'reading', 'overall',
        ]


class GMATCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.GMATCertificate
        fields = [
            'id', 'analytical_writing_assessment', 'integrated_reasoning', 'quantitative_and_verbal', 'total'
        ]


class GRECertificateSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.GRECertificate
        fields = [
            'id', 'quantitative', 'verbal', 'analytical_writing',
        ]


class StudentDetailedInfoSerializer(serializers.ModelSerializer):
    from sNeeds.apps.customAuth.serializers import SafeUserDataSerializer
    user = SafeUserDataSerializer(read_only=True)

    apply_semester_year = StudentFormApplySemesterYearCustomPrimaryKeyRelatedField(
        many=False,
        queryset=StudentFormApplySemesterYear.objects.all()
    )

    gre_certificate = GRECertificateSerializer()
    gmat_certificate = GMATCertificateSerializer()

    marital_status = BasicFormFieldSerializer()
    payment_affordability = BasicFormFieldSerializer()

    universities = serializers.SerializerMethodField()
    language_certificates = serializers.SerializerMethodField()
    want_to_applies = serializers.SerializerMethodField
    publications = serializers.SerializerMethodField()

    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user',
            'age', 'marital_status',
            'universities', 'want_to_applies', 'publications',
            'language_certificates', 'gre_certificate', 'gmat_certificate',
            'payment_affordability', 'prefers_full_fund', 'prefers_half_fun', 'prefers_self_fund',
            'comment', 'resume', 'related_work_experience', 'academic_break', 'olympiad', 'powerful_recommendation',
            'linkedin_url', 'homepage_url',
            'created', 'updated',
        ]

    def get_universities(self, obj):
        qs = FormUniversityThrough.objects.filter(student_detailed_info_id=obj.id)
        return FormUniversityThroughSerializer(qs, many=True, context=self.context).data

    def get_language_certificates(self, obj):
        qs = LanguageCertificateTypeThrough.objects.filter(student_detailed_info_id=obj.id)
        return LanguageCertificateTypeThroughSerializer(qs, many=True, context=self.context).data

    def get_want_to_applies(self, obj):
        qs = WantToApply.objects.filter(student_detailed_info_id=obj.id)
        return WantToApplySerializer(qs, many=True, context=self.context).data

    def get_publications(self, obj):
        qs = Publication.objects.filter(student_detailed_info_id=obj.id)
        return PublicationSerializer(qs, many=True, context=True)

    def validate(self, attrs):
        # if attrs.get('grade').category != 'grade':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('grade', 'grade')))
        # if attrs.get('apply_grade').category != 'apply_grade':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('apply_grade', 'apply_grade')))
        # if attrs.get('apply_country').category != 'apply_country':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('apply_country', 'apply_country')))
        # if attrs.get('apply_mainland').category != 'apply_mainland':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('apply_mainland', 'apply_mainland')))
        # if attrs.get('marital_status').category != 'marital_status':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('marital_status', 'marital_status')))
        # if attrs.get('language_certificate').category != 'language_certificate':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('language_certificate', 'language_certificate')))
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        if user.is_consultant():
            raise ValidationError(_("Consultants can not create Student Detailed Info"))
        user_student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if user_student_detailed_info_qs.exists():
            raise ValidationError(_("User already has student detailed info"))
        student_detailed_info_obj = StudentDetailedInfo.objects.create(user=user, **validated_data)
        return student_detailed_info_obj


class StudentDetailedInfoRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user',
            'age', 'marital_status',
            'universities', 'want_to_applies', 'publications',
            'language_certificates', 'gre_certificate', 'gmat_certificate',
            'payment_affordability', 'prefers_full_fund', 'prefers_half_fun', 'prefers_self_fund',
            'comment', 'resume', 'related_work_experience', 'academic_break', 'olympiad', 'powerful_recommendation',
            'linkedin_url', 'homepage_url',
            'created', 'updated',
        ]

    def validate(self, attrs):
        # if attrs.get('grade').category != 'grade':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('grade', 'grade')))
        # if attrs.get('apply_grade').category != 'apply_grade':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('apply_grade', 'apply_grade')))
        # if attrs.get('apply_country').category != 'apply_country':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('apply_country', 'apply_country')))
        # if attrs.get('apply_mainland').category != 'apply_mainland':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('apply_mainland', 'apply_mainland')))
        # if attrs.get('marital_status').category != 'marital_status':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('marital_status', 'marital_status')))
        # if attrs.get('language_certificate').category != 'language_certificate':
        #     raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}"
        #                             .format('language_certificate', 'language_certificate')))
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        if user.is_consultant():
            raise ValidationError(_("Consultants can not create Student Detailed Info"))
        user_student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if user_student_detailed_info_qs.exists():
            raise ValidationError(_("User already has student detailed info"))
        student_detailed_info_obj = StudentDetailedInfo.objects.create(user=user, **validated_data)
        return student_detailed_info_obj
