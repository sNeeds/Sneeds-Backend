from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.request import Request

from abroadin.apps.data.account.models import BasicFormField, University, Major
from abroadin.apps.data.account.serializers import UniversitySerializer, MajorSerializer
from abroadin.base.api.fields import GenericContentTypeRelatedField, GenericContentObjectRelatedURL
from abroadin.base.api.serializers import generic_hyperlinked_related_method

from .models import (
    SemesterYear, Publication, Grade, Education, LanguageCertificate,
    RegularLanguageCertificate, GMATCertificate, GREGeneralCertificate, GRESubjectCertificate, GREPhysicsCertificate,
    GREBiologyCertificate, GREPsychologyCertificate, DuolingoCertificate)

from abroadin.apps.estimation.form.models import StudentDetailedInfo

from abroadin.apps.applyprofile.models import ApplyProfile

LCType = LanguageCertificate.LanguageCertificateType


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
    related_classes = []

    content_type = GenericContentTypeRelatedField()
    content_url = GenericContentObjectRelatedURL()

    class Meta:
        model = Publication
        abstract = True
        fields = [
            'id', 'title', 'publish_year', 'which_author', 'type', 'journal_reputation',
            'content_type', 'object_id', 'content_url',
        ]

        extra_kwargs = {
            # 'content_object': {'read_only': True},
        }


class PublicationRequestSerializer(serializers.ModelSerializer):
    related_classes = []

    content_type = GenericContentTypeRelatedField()

    class Meta:
        model = Publication
        fields = [
            'id', 'content_object', 'title', 'publish_year', 'which_author', 'type', 'journal_reputation',
            'content_type', 'object_id',
        ]


class EducationSerializer(serializers.ModelSerializer):
    related_classes = []

    content_type = GenericContentTypeRelatedField()
    content_url = GenericContentObjectRelatedURL()

    class Meta:
        model = Education
        fields = [
            'id', 'university', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
            'content_type', 'object_id', 'content_url',
        ]

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class EducationRequestSerializer(serializers.ModelSerializer):
    related_classes = []

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

    content_type = GenericContentTypeRelatedField()

    # content_url = GenericContentObjectRelatedURL()

    class Meta:
        model = Education
        fields = [
            'id', 'university', 'content_object', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
            'content_type', 'object_id',
        ]


class LanguageCertificateSerializer(serializers.ModelSerializer):
    related_classes = []

    content_type = GenericContentTypeRelatedField()


    class Meta:
        model = LanguageCertificate
        fields = '__all__'



class RegularLanguageCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = RegularLanguageCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LCType.IELTS_ACADEMIC, LCType.IELTS_GENERAL,
                         LCType.TOEFL]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class RegularLanguageCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularLanguageCertificate
        validators = []
        fields = '__all__'
        # # exclude = ['content_object']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GMATCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GMATCertificate
        fields = '__all__'
        # exclude = ['content_object']

    def validate_certificate_type(self, value):
        if value not in [LCType.GMAT]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GMATCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GMATCertificate
        validators = []
        fields = '__all__'
        # exclude = ['content_object']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GREGeneralCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GREGeneralCertificate
        fields = '__all__'
        # exclude = ['content_object']

    def validate_certificate_type(self, value):
        if value not in [LCType.GRE_GENERAL]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREGeneralCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GREGeneralCertificate
        validators = []
        fields = '__all__'
        # exclude = ['content_object']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GRESubjectCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GRESubjectCertificate
        fields = '__all__'
        # exclude = ['content_object']

    def validate_certificate_type(self, value):
        if value not in [LCType.GRE_CHEMISTRY, LCType.GRE_LITERATURE,
                         LCType.GRE_MATHEMATICS]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GRESubjectCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GRESubjectCertificate
        validators = []
        fields = '__all__'
        # exclude = ['content_object']

    default_validators = []

    def validate(self, attrs):
        return attrs


class GREBiologyCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GREBiologyCertificate
        fields = '__all__'
        # exclude = ['content_object']

    def validate_certificate_type(self, value):
        if value not in [LCType.GRE_BIOLOGY]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREPhysicsCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GREPhysicsCertificate
        fields = '__all__'
        # exclude = ['content_object']

    def validate_certificate_type(self, value):
        if value not in [LCType.GRE_PHYSICS]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREPsychologyCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GREPsychologyCertificate
        fields = '__all__'
        # exclude = ['content_object']

    def validate_certificate_type(self, value):
        if value not in [LCType.GRE_PSYCHOLOGY]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class DuolingoCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = DuolingoCertificate
        fields = '__all__'
        # exclude = ['content_object']

    def validate_certificate_type(self, value):
        if value not in [LCType.DUOLINGO]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class DuolingoCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = DuolingoCertificate
        validators = []
        fields = '__all__'
        # exclude = ['content_object']

    default_validators = []

    def validate(self, attrs):
        return attrs


def serialize_language_certificates(queryset, parent_serializer, related_classes):
    """
    parameter: queryset is a queryset of parent LanguageCertificate objects
    """
    ret = {}
    ret2 = []

    for obj in queryset:
        if obj.certificate_type in [LCType.TOEFL, LCType.IELTS_GENERAL, LCType.IELTS_ACADEMIC]:
            serializer = RegularLanguageCertificateSerializer(obj.regularlanguagecertificate,
                                                              many=False,
                                                              context=parent_serializer.context)

        elif obj.certificate_type in [LCType.GMAT]:
            serializer = GMATCertificateSerializer(obj.gmatcertificate,
                                                   many=False,
                                                   context=parent_serializer.context)

        elif obj.certificate_type in [LCType.GRE_GENERAL]:
            serializer = GREGeneralCertificateSerializer(obj.gregeneralcertificate,
                                                         many=False,
                                                         context=parent_serializer.context)

        elif obj.certificate_type in [LCType.GRE_CHEMISTRY, LCType.GRE_LITERATURE, LCType.GRE_MATHEMATICS]:
            serializer = GRESubjectCertificateSerializer(obj.gresubjectcertificate,
                                                         many=False,
                                                         context=parent_serializer.context)

        elif obj.certificate_type in [LCType.GRE_BIOLOGY]:
            serializer = GREBiologyCertificateSerializer(obj.gresubjectcertificate.grebiologycertificate,
                                                         many=False,
                                                         context=parent_serializer.context)

        elif obj.certificate_type in [LCType.GRE_PHYSICS]:
            serializer = GREPhysicsCertificateSerializer(obj.gresubjectcertificate.grephysicscertificate,
                                                         many=False,
                                                         context=parent_serializer.context)

        elif obj.certificate_type in [LCType.GRE_PSYCHOLOGY]:
            serializer = GREPsychologyCertificateSerializer(obj.gresubjectcertificate.grepsychologycertificate,
                                                            many=False,
                                                            context=parent_serializer.context)

        elif obj.certificate_type in [LCType.DUOLINGO]:
            serializer = DuolingoCertificateSerializer(obj.duolingocertificate,
                                                       many=False,
                                                       context=parent_serializer.context)

        serializer.related_classes = related_classes
        ret[obj.certificate_type] = serializer.data
        ret2.append(serializer.data)
    return ret2
