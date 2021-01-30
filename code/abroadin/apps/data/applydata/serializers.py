from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from abroadin.apps.data.account.models import BasicFormField
from abroadin.apps.data.account.serializers import UniversitySerializer, MajorSerializer
from abroadin.base.api.fields import GenericContentTypeRelatedField, _get_content_type_identifier
from abroadin.base.values import AccessibilityTypeChoices
from abroadin.base.factory.class_factory import exclude_meta_fields_class_factory

from .models import (
    SemesterYear, Publication, Grade, Education, LanguageCertificate,
    RegularLanguageCertificate, GMATCertificate, GREGeneralCertificate, GRESubjectCertificate, GREPhysicsCertificate,
    GREBiologyCertificate, GREPsychologyCertificate, DuolingoCertificate)
from abroadin.apps.estimation.form.models import StudentDetailedInfo

LCType = LanguageCertificate.LanguageCertificateType


def get_certificate_class_serializer(certificate_class):
    model_serializer_map = {
        "regularlanguagecertificate": RegularLanguageCertificateSerializer,
        "gmatcertificate": GMATCertificateSerializer,
        "gregeneralcertificate": GREGeneralCertificateSerializer,
        "gresubjectcertificate": GRESubjectCertificateSerializer,
        "grebiologycertificate": GREBiologyCertificateSerializer,
        "grephysicscertificate": GREPhysicsCertificateSerializer,
        "grepsychologycertificate": GREPsychologyCertificateSerializer,
        "duolingocertificate": DuolingoCertificateSerializer
    }

    certificate_class_name = certificate_class.__name__.lower()
    serializer_class = model_serializer_map.get(certificate_class_name)

    if not serializer_class:
        raise ValueError(f"Can't find match to model {certificate_class_name} in model serializer map")

    return serializer_class


def serialize_language_certificates(queryset, parent_serializer, related_classes,
                                    mapper_func=get_certificate_class_serializer, **kwargs):
    """
    parameter: queryset is a queryset of parent LanguageCertificate objects
    """

    ret = {}
    ret2 = []

    for obj in queryset:
        obj = obj.cast()
        serializer_class = mapper_func(obj.__class__)
        serializer = serializer_class(obj, context=parent_serializer.context)
        serializer.related_classes = related_classes
        ret[obj.certificate_type] = serializer.data
        ret2.append(serializer.data)

    if kwargs.pop('dict_output', False):
        return ret
    return ret2


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ["id", "name"]


class LockedGradeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, default="*", source=' ')
    name = serializers.CharField(read_only=True, default="*", source=' ')
    accessibility_type = serializers.CharField(read_only=True, default=AccessibilityTypeChoices.LOCKED, source=' ')

    class Meta:
        model = Grade
        fields = ["id", "name",
                  'accessibility_type',
                  ]


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

    class Meta:
        model = Publication
        abstract = True
        fields = [
            'id', 'title', 'publish_year', 'which_author', 'type', 'journal_reputation',
            'content_type', 'object_id',
        ]


class EducationSerializer(serializers.ModelSerializer):
    related_classes = []

    content_type = GenericContentTypeRelatedField()

    class Meta:
        model = Education
        fields = [
            'id', 'university', 'grade', 'major', 'graduate_in', 'thesis_title', 'gpa',
            'content_type', 'object_id',
        ]

    def create(self, validated_data):
        raise ValidationError(_("Creating object through this serializer is not allowed"))


class EducationDetailedRepresentationSerializer(EducationSerializer):
    class Meta(EducationSerializer.Meta):
        pass

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        context = {"request": self.context.get("request")}

        ret["university"] = UniversitySerializer(instance.university, context=context).data
        ret["major"] = MajorSerializer(instance.major, context=context).data

        return ret


class LanguageCertificateSerializer(serializers.ModelSerializer):
    # TODO: Makes program decoupled, Can we change this?
    related_classes = [
        {'model_class': StudentDetailedInfo}
    ]

    content_type = GenericContentTypeRelatedField()

    class Meta:
        model = LanguageCertificate
        fields = ['certificate_type', 'is_mock', 'content_type', 'object_id']


class LanguageCertificateInheritedSerializer(serializers.Serializer):
    related_classes = [
        {'model_class': RegularLanguageCertificate, },
    ]  # Currently RegularLanguageCertificate is supported

    class_type = GenericContentTypeRelatedField()
    data = serializers.DictField(allow_empty=False)

    class Meta:
        fields = ['certificate_type', 'data']

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        content_type = internal_value.get('class_type')
        model_class = content_type.model_class()

        serializer_class = get_certificate_class_serializer(model_class)
        exclude_fields = {"content_type", "object_id"}
        SerializerClass = exclude_meta_fields_class_factory(serializer_class, exclude_fields)
        serializer = SerializerClass(data=internal_value.get('data'))
        serializer.is_valid(raise_exception=True)

        return internal_value

    def to_representation(self, instance):
        ret = OrderedDict()
        instance = instance.cast()

        content_type = ContentType.objects.get_for_model(instance)
        model_class = content_type.model_class()

        SerializerClass = get_certificate_class_serializer(model_class)
        serializer = SerializerClass(instance)

        ret['class_type'] = _get_content_type_identifier(content_type)
        ret['data'] = serializer.data

        return ret


class RegularLanguageCertificateSerializer(LanguageCertificateSerializer):
    class Meta(LanguageCertificateSerializer.Meta):
        model = RegularLanguageCertificate
        fields = LanguageCertificateSerializer.Meta.fields + [
            'listening', 'writing', 'speaking', 'reading', 'overall'
        ]

    def validate_certificate_type(self, value):
        if value not in [
            LCType.IELTS_ACADEMIC, LCType.IELTS_GENERAL, LCType.TOEFL
        ]:
            raise ValidationError(_("Value is not in allowed certificate types."))

        return value


class RegularLanguageCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularLanguageCertificate
        validators = []
        fields = '__all__'

    default_validators = []

    def validate(self, attrs):
        return attrs


class GMATCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GMATCertificate
        fields = '__all__'

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

    def validate_certificate_type(self, value):
        if value not in [LCType.GRE_GENERAL]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREGeneralCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GREGeneralCertificate
        validators = []
        fields = '__all__'

    default_validators = []

    def validate(self, attrs):
        return attrs


class GRESubjectCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GRESubjectCertificate
        fields = '__all__'

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

    def validate_certificate_type(self, value):
        if value not in [LCType.GRE_BIOLOGY]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREPhysicsCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GREPhysicsCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LCType.GRE_PHYSICS]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class GREPsychologyCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = GREPsychologyCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LCType.GRE_PSYCHOLOGY]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class DuolingoCertificateSerializer(LanguageCertificateSerializer):
    class Meta:
        model = DuolingoCertificate
        fields = '__all__'

    def validate_certificate_type(self, value):
        if value not in [LCType.DUOLINGO]:
            raise ValidationError(_("Value is not in allowed certificate types."))
        return value


class DuolingoCertificateCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = DuolingoCertificate
        validators = []
        fields = '__all__'

    default_validators = []

    def validate(self, attrs):
        return attrs
