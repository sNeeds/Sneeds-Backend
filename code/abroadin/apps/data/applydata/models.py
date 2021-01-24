from math import floor

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from abroadin.apps.data.account.models import University, Major, Country
from abroadin.apps.data.account.validators import ten_factor_validator
from abroadin.apps.data.applydata.classes import ValueRange
from abroadin.apps.data.applydata.decorators import regular_certificate_or_none
from abroadin.apps.data.applydata.managers import EducationManager, GradeManager, \
    PublicationManager, LanguageCertificateManager
from abroadin.apps.data.applydata.validators import validate_ielts_score, validate_toefl_overall_score, \
    validate_toefl_section_score
from abroadin.apps.data.applydata.values import VALUES_WITH_ATTRS
from abroadin.base.mixins.validators import GenericForeignkeyUniqueTogetherValidationMixin
from abroadin.base.models.abstracts import InheritanceCastModel

SDI_CT = ContentType.objects.get(app_label='form', model='studentdetailedinfo')


class GradeChoices(models.TextChoices):
    # Don't change order
    BACHELOR = 'Bachelor', 'Bachelor'
    MASTER = 'Master', 'Master'
    PHD = 'PH.D', 'PH.D'
    POST_DOC = 'Post Doc', 'Post Doc'

    @classmethod
    def get_ordered(cls):
        """
        From low to high. e.g. Bachelor, Master, ...
        """
        return cls.values

    @classmethod
    def order_num(cls, grade):
        return cls.values.index(grade)

    @classmethod
    def higher_grade_or_same(cls, grade):
        next_grade_index = min(cls.order_num(grade) + 1, len(cls.values) - 1)
        return cls.values[next_grade_index]


class SemesterYear(models.Model):
    class SemesterChoices(models.TextChoices):
        SPRING = "Spring"
        SUMMER = "Summer"
        FALL = "Fall"
        WINTER = "Winter"

    year = models.SmallIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        help_text="In Gregorian"
    )
    semester = models.CharField(
        max_length=64,
        choices=SemesterChoices.choices
    )

    class Meta:
        ordering = ["year", "semester"]

    def __str__(self):
        return str(self.year) + " " + self.semester


class Grade(models.Model):
    name = models.CharField(
        max_length=128,
        choices=GradeChoices.choices,
        default=GradeChoices.BACHELOR,
        unique=True
    )

    objects = GradeManager.as_manager()

    def __str__(self):
        return self.name.__str__()


class Education(GenericForeignkeyUniqueTogetherValidationMixin, models.Model):
    content_type_based_uniqueness_check_fields = {
        'content_type': {
            'form__studentdetailedinfo': ['object_id', 'grade'],
            'form__studentdetailedinfobase': ['object_id', 'grade'],
        }
    }
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE
    )

    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type', 'object_id',
    )

    university = models.ForeignKey(
        University, on_delete=models.PROTECT
    )
    grade = models.CharField(
        max_length=128,
        choices=GradeChoices.choices,
        default=GradeChoices.BACHELOR
    )
    major = models.ForeignKey(
        Major, on_delete=models.PROTECT
    )
    graduate_in = models.SmallIntegerField(
        validators=[MinValueValidator(1980), MaxValueValidator(2100)],
        help_text="In Gregorian"
    )
    thesis_title = models.CharField(
        max_length=512,
        blank=True,
        null=True
    )
    gpa = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        max_digits=4,
        decimal_places=2
    )
    value = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        null=True,
        editable=False
    )

    objects = EducationManager.as_manager()

    GPA_STORE_LABEL_RANGE = 0.25
    GPA_VIEW_LABEL_RANGE = 1
    GPA_MAX_ALLOWED = 20

    @property
    def gpa_value(self):
        if self.gpa < 13:
            val = 0
        elif 13 <= self.gpa < 16:
            val = self.gpa / 28
        elif 16 <= self.gpa < 18:
            val = self.gpa / 23
        else:
            val = self.gpa / 20
        return float(val)

    def compute_value(self):
        return round(self.university.value * self.gpa_value, 2)

    def get_value_label(self):
        value_range = ValueRange(VALUES_WITH_ATTRS["university_through"])
        label = value_range.find_value_attrs(self.value, 'label')

        return label

    #############################
    # Grade Point Average methods
    #############################
    def get_gpa__store_label(self):
        item_range = self.GPA_STORE_LABEL_RANGE
        value = float(self.gpa)
        if value >= self.GPA_MAX_ALLOWED:
            value -= 0.03
        return str(floor(value / item_range) * item_range)

    def get_gpa__view_label(self):
        if self.gpa < 12:
            return '-12'
        value = float(self.gpa)
        if value >= self.GPA_MAX_ALLOWED:
            value -= 0.03
        item_range = self.GPA_VIEW_LABEL_RANGE
        value = floor(value / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def convert_gpa_store_to_view_label(cls, label):
        input_value = float(label)
        if input_value < 12:
            return '-12'
        if input_value >= cls.GPA_MAX_ALLOWED:
            input_value -= 0.03
        item_range = cls.GPA_VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def get_gpa_user_store_based_positions(cls, sdi):
        user_last_grade = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id) \
            .order_by('-graduate_in').first()
        if user_last_grade is None:
            return ['0.0']
        return [user_last_grade.get_gpa__store_label()]

    @classmethod
    def get_gpa_user_view_based_positions(cls, sdi):
        user_last_grade = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id) \
            .order_by('-graduate_in').first()
        if user_last_grade is None:
            return None
        return [user_last_grade.get_gpa__view_label()]

    @classmethod
    def compare_gpa_labels(cls, label1, label2):
        if float(label1) >= float(label2):
            return label1
        return label2

    @classmethod
    def get_gpa__store_label_rank(cls, label):
        return float(label)


class Publication(models.Model):
    class WhichAuthorChoices(models.TextChoices):
        FIRST = 'First', 'First'
        SECOND = 'Second', 'Second'
        THIRD = 'Third', 'Third'
        FOURTH_OR_MORE = 'Fourth or more', 'Fourth or more'

    class PublicationChoices(models.TextChoices):
        JOURNAL = 'Journal'
        CONFERENCE = 'Conference'

    class JournalReputationChoices(models.TextChoices):
        ONE_TO_THREE = 'One to three', 'One to three'
        FOUR_TO_TEN = 'Four to ten', 'Four to ten'
        ABOVE_TEN = 'Above ten', 'Above ten'

    PUBLICATIONS_SCORE__STORE_LABEL_RANGE = 0.1
    PUBLICATIONS_SCORE__VIEW_LABEL_RANGE = 0.2

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type', 'object_id',
    )

    title = models.CharField(max_length=512)
    publish_year = models.SmallIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        help_text="In Gregorian"
    )
    which_author = models.CharField(
        choices=WhichAuthorChoices.choices,
        max_length=128,
        default=WhichAuthorChoices.FOURTH_OR_MORE
    )
    type = models.CharField(
        choices=PublicationChoices.choices,
        max_length=20,
        default=PublicationChoices.JOURNAL
    )
    journal_reputation = models.CharField(
        max_length=128,
        choices=JournalReputationChoices.choices,
    )

    value = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        editable=False
    )  # Updated in signal

    objects = PublicationManager.as_manager()

    def __str__(self):
        return self.title

    MAX_ALLOWED_PUBLICATIONS_SCORE = 1.0

    ############################
    # Publications Count methods
    ############################
    def get_count_chart__store_label(self):
        # TODO Change coed to be consistence with new form structure
        return str(self.content_object.publication_set.count())

    @classmethod
    def get_publication_count_user_store_based_positions(cls, sdi):
        return [str(cls.objects.filter(content_type=SDI_CT, object_id=sdi.id).count())]

    @classmethod
    def get_publication_count_user_view_based_positions(cls, sdi):
        return [cls.convert_count_chart_store_to_view_label(
            str(cls.objects.filter(content_type=SDI_CT, object_id=sdi.id).count()))
        ]

    @classmethod
    def convert_count_chart_store_to_view_label(cls, label):
        count = int(label)
        if count <= 3:
            return label
        if count >= 4:
            return '4+'

    @classmethod
    def compare_publication_count_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2

    @classmethod
    def get_publications_count__store_label_rank(cls, label):
        return float(label)

    ##########################
    # Publication Type methods
    ##########################
    def get_type__store_label(self):
        return self.type

    def get_type__view_label(self):
        return self.type

    @classmethod
    def get_publication_type_user_store_based_positions(cls, sdi):
        qs = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)
        positions = []

        for obj in qs:
            positions.append(obj.get_type__store_label())
        return positions

    @classmethod
    def get_publication_type_user_view_based_positions(cls, sdi):
        qs = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)
        positions = []

        for obj in qs:
            positions.append(obj.get_type__view_label())
        return positions

    ###################################
    # Publication Impact factor methods
    ###################################
    def get_impact_factor__store_label(self):
        return self.journal_reputation

    def get_impact_factor__view_label(self):
        return self.journal_reputation

    @classmethod
    def get_publication_impact_factor_user_store_based_positions(cls, sdi):
        qs = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)
        positions = []

        for obj in qs:
            positions.append(obj.get_impact_factor__store_label())
        return positions

    @classmethod
    def get_publication_impact_factor_user_view_based_positions(cls, sdi):
        qs = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)
        positions = []

        for obj in qs:
            positions.append(obj.get_impact_factor__view_label())
        return positions

    @classmethod
    def compare_publication_impact_factor_labels(cls, label1, label2):
        if (label1 == cls.JournalReputationChoices.ONE_TO_THREE) or \
                (
                        label1 == cls.JournalReputationChoices.FOUR_TO_TEN and label2 == cls.JournalReputationChoices.ABOVE_TEN):
            return label1

        elif (label1 == cls.JournalReputationChoices.ABOVE_TEN) or \
                (
                        label1 == cls.JournalReputationChoices.FOUR_TO_TEN and label2 == cls.JournalReputationChoices.ONE_TO_THREE):
            return label2
        return label1

    @classmethod
    def get_impact_factor__store_label_rank(cls, label):
        if label == cls.JournalReputationChoices.ONE_TO_THREE:
            return 1
        elif label == cls.JournalReputationChoices.FOUR_TO_TEN:
            return 5
        elif label == cls.JournalReputationChoices.ABOVE_TEN:
            return 10
        return 0

    ############################
    # Publications Score methods
    ############################
    @classmethod
    def get_publications_score__store_label(cls, value):
        if value >= cls.MAX_ALLOWED_PUBLICATIONS_SCORE:
            value -= 0.03
        item_range = cls.PUBLICATIONS_SCORE__STORE_LABEL_RANGE
        return str(floor(value / item_range) * item_range)

    @classmethod
    def get_publications_score__view_label(cls, input_value):
        if input_value >= cls.MAX_ALLOWED_PUBLICATIONS_SCORE:
            input_value -= 0.03
        item_range = cls.PUBLICATIONS_SCORE__VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def convert_publications_score__store_to_view_label(cls, label):
        input_value = float(label)
        if input_value >= cls.MAX_ALLOWED_PUBLICATIONS_SCORE:
            input_value -= 0.03
        item_range = cls.PUBLICATIONS_SCORE__VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def get_publications_score_user_store_based_positions(cls, sdi):
        qs = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)
        positions = [cls.get_publications_score__store_label(qs.total_value())]
        return positions

    @classmethod
    def get_publications_score_user_view_based_positions(cls, sdi):
        qs = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)
        positions = [cls.get_publications_score__view_label(qs.total_value())]
        return positions

    @classmethod
    def compare_publications_score_labels(cls, label1, label2):
        if float(label1) >= float(label2):
            return label1
        return label2

    @classmethod
    def get_publications_score__store_label_rank(cls, label):
        return float(label)


class LanguageCertificate(
    InheritanceCastModel,
    GenericForeignkeyUniqueTogetherValidationMixin,
    models.Model
):
    class LanguageCertificateType(models.TextChoices):
        IELTS_GENERAL = 'IELTS General', 'IELTS General'
        IELTS_ACADEMIC = 'IELTS Academic', 'IELTS Academic'
        TOEFL = 'TOEFL', 'TOEFL'
        GMAT = 'GMAT', 'GMAT'
        GRE_GENERAL = 'GRE General', 'GRE General'
        GRE_CHEMISTRY = 'GRE Chemistry', 'GRE Chemistry'
        GRE_MATHEMATICS = 'GRE Mathematics', 'GRE Mathematics'
        GRE_LITERATURE = 'GRE Literature', 'GRE Literature'
        GRE_BIOLOGY = 'GRE Biology', 'GRE Biology'
        GRE_PHYSICS = 'GRE Physics', 'GRE Physics'
        GRE_PSYCHOLOGY = 'GRE Psychology', 'GRE Psychology'
        DUOLINGO = 'Duolingo', 'Duolingo'

    content_type_based_uniqueness_check_fields = {
        'content_type': {
            'form__studentdetailedinfo': ['object_id', 'certificate_type'],
            'form__studentdetailedinfobase': ['object_id', 'certificate_type'],
        }
    }

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='language_certificates'
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type', 'object_id',
    )

    certificate_type = models.CharField(
        choices=LanguageCertificateType.choices,
        default=LanguageCertificateType.TOEFL,
        max_length=64,
        help_text="Based on endpoint just some types are allowed to insert not all certificate types."
    )
    is_mock = models.BooleanField(
        default=False
    )

    objects = LanguageCertificateManager.as_manager()

    class Meta:
        unique_together = ('certificate_type', 'content_type', 'object_id')

    @regular_certificate_or_none
    def _get_key_in_values_with_attrs(self):
        """
        Returns key(label) in VALUES_WITH_ATTRS dictionary.
        """
        if self.certificate_type == self.LanguageCertificateType.TOEFL:
            value_label = "toefl"
        elif self.certificate_type in {
            self.LanguageCertificateType.IELTS_GENERAL,
            self.LanguageCertificateType.IELTS_ACADEMIC
        }:
            value_label = "ielts_academic_and_general"

        return value_label

    def is_regular_language_certificate_instance(self):
        try:
            self.regularlanguagecertificate
            return True
        except RegularLanguageCertificate.DoesNotExist:
            return False

    @property
    @regular_certificate_or_none
    def value_label(self):
        key = self._get_key_in_values_with_attrs()

        overall = self.regularlanguagecertificate.overall

        value_range = ValueRange(VALUES_WITH_ATTRS[key])
        label = value_range.find_value_attrs(overall, 'label')

        return label

    @property
    @regular_certificate_or_none
    def value(self):
        key = self._get_key_in_values_with_attrs()

        overall = self.regularlanguagecertificate.overall

        value_range = ValueRange(VALUES_WITH_ATTRS[key])
        value = value_range.find_value_attrs(overall, 'value')

        return value

    def brief_str(self):
        if self.is_regular_language_certificate_instance():
            regular_certificate = self.regularlanguagecertificate
            return self.certificate_type + " " + str(regular_certificate.overall)

        return None

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class RegularLanguageCertificate(LanguageCertificate):
    speaking = models.DecimalField(max_digits=4, decimal_places=1,
                                   help_text=" IELTS speaking 0 to 9 and TOEFL speaking 0 to 30")

    listening = models.DecimalField(max_digits=4, decimal_places=1,
                                    help_text=" IELTS listening 0 to 9 and TOEFL listening 0 to 30")

    writing = models.DecimalField(max_digits=4, decimal_places=1,
                                  help_text=" IELTS writing 0 to 9 and TOEFL writing 0 to 30")

    reading = models.DecimalField(max_digits=4, decimal_places=1,
                                  help_text=" IELTS reading 0 to 9 and TOEFL reading 0 to 30")

    overall = models.DecimalField(max_digits=4, decimal_places=1,
                                  help_text=" IELTS overall 1 to 9 and TOEFL overall 0 to 120")

    def clean(self, *args, **kwargs):
        if self.certificate_type not in [LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC,
                                         LanguageCertificate.LanguageCertificateType.IELTS_GENERAL,
                                         LanguageCertificate.LanguageCertificateType.TOEFL]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})

        if self.certificate_type in [LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC,
                                     LanguageCertificate.LanguageCertificateType.IELTS_GENERAL]:
            validate_ielts_score(self.speaking)
            validate_ielts_score(self.listening)
            validate_ielts_score(self.writing)
            validate_ielts_score(self.reading)
            validate_ielts_score(self.overall)

        if self.certificate_type in [LanguageCertificate.LanguageCertificateType.TOEFL]:
            validate_toefl_overall_score(self.overall)
            validate_toefl_section_score(self.speaking)
            validate_toefl_section_score(self.listening)
            validate_toefl_section_score(self.writing)
            validate_toefl_section_score(self.reading)

    # IELTS overall 0 to 9
    # TOEFL overall 0 to 120
    IELTS__STORE_LABEL_RANGE = 0.5
    IELTS__VIEW_LABEL_RANGE = 1
    TOEFL__STORE_LABEL_RANGE = 10
    TOEFL__VIEW_LABEL_RANGE = 20

    ###############
    # IELTS methods
    ###############
    def get_ielts__store_label(self):
        item_range = self.IELTS__STORE_LABEL_RANGE
        return str(floor(float(self.overall) / item_range) * item_range)

    def get_ielts__view_label(self):
        item_range = self.IELTS__VIEW_LABEL_RANGE
        value = floor(float(self.overall) / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def convert_ielts_store_to_view_label(cls, label):
        input_value = float(label)
        item_range = cls.IELTS__VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def get_ielts_user_store_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id).filter(
            Q(certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_GENERAL) |
            Q(certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC)
        ).distinct()

        for obj in user_toefl_certificates:
            positions.append(obj.get_ielts__store_label())

        return positions

    @classmethod
    def get_ielts_user_view_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(
            Q(content_type=SDI_CT, object_id=sdi.id) and
            (Q(certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_GENERAL) or
             Q(certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC))
        )

        for obj in user_toefl_certificates:
            positions.append(obj.get_ielts__view_label())

        return positions

    @classmethod
    def compare_ielts_labels(cls, label1, label2):
        if float(label1) >= float(label2):
            return label1
        return label2

    @classmethod
    def get_ielts__store_label_rank(cls, label):
        return float(label)

    ###############
    # TOEFL methods
    ###############
    def get_toefl__store_label(self):
        item_range = self.TOEFL__STORE_LABEL_RANGE
        return str(floor(float(self.overall) / item_range) * item_range)

    def get_toefl__view_label(self):
        item_range = self.TOEFL__VIEW_LABEL_RANGE
        value = floor(float(self.overall) / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def convert_toefl_store_to_view_label(cls, label):
        input_value = int(label)
        item_range = cls.TOEFL__VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def get_toefl_user_store_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id,
                                                     certificate_type=LanguageCertificate.LanguageCertificateType.TOEFL
                                                     )
        for obj in user_toefl_certificates:
            positions.append(obj.get_toefl__store_label())

        return positions

    @classmethod
    def get_toefl_user_view_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(
            content_type=SDI_CT, object_id=sdi.id,
            certificate_type=LanguageCertificate.LanguageCertificateType.TOEFL
        )
        for obj in user_toefl_certificates:
            positions.append(obj.get_toefl__view_label())

        return positions

    @classmethod
    def compare_toefl_labels(cls, label1, label2):
        if float(label1) >= float(label2):
            return label1
        return label2

    @classmethod
    def get_toefl__store_label_rank(cls, label):
        return float(label)


class GMATCertificate(LanguageCertificate):
    analytical_writing_assessment = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(6.00)],
    )
    integrated_reasoning = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
    )
    quantitative_and_verbal = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(51)],
    )
    total = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(200), MaxValueValidator(800)],
    )

    TOTAL_STORE_LABEL_RANGE = 20
    TOTAL_VIEW_LABEL_RANGE = 100

    def clean(self, *args, **kwargs):
        if self.certificate_type not in [LanguageCertificate.LanguageCertificateType.GMAT]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})

    def get_store_label(self):
        item_range = self.TOTAL_STORE_LABEL_RANGE
        return str(floor(self.total / item_range) * item_range)

    def get_view_label(self):
        item_range = self.TOTAL_VIEW_LABEL_RANGE
        value = floor(self.total / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def convert_store_to_view_label(cls, label):
        input_value = int(label)
        item_range = cls.TOTAL_VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def get_user_store_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)
        for obj in user_toefl_certificates:
            positions.append(obj.get_store_label())

        return positions

    @classmethod
    def get_user_view_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)
        for obj in user_toefl_certificates:
            positions.append(obj.get_view_label())

        return positions

    @classmethod
    def compare_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2

    @classmethod
    def get_store_label_rank(cls, label):
        return float(label)


class GREGeneralCertificate(LanguageCertificate):
    quantitative = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(130), MaxValueValidator(170)],
    )
    verbal = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(130), MaxValueValidator(170)],
    )
    analytical_writing = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
    )

    def clean(self, *args, **kwargs):
        if self.certificate_type not in [LanguageCertificate.LanguageCertificateType.GRE_GENERAL]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})

    WRITING_STORE_LABEL_RANGE = 0.5
    WRITING_VIEW_LABEL_RANGE = 1
    Q_AND_V_STORE_LABEL_RANGE = 10
    Q_AND_V_VIEW_LABEL_RANGE = 20

    #################
    # Writing methods
    #################
    def get_writing_store_label(self):
        item_range = self.WRITING_STORE_LABEL_RANGE
        return str(floor(float(self.analytical_writing) / item_range) * item_range)

    def get_writing_view_label(self):
        item_range = self.WRITING_VIEW_LABEL_RANGE
        value = floor(float(self.analytical_writing) / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def convert_writing_store_to_view_label(cls, label):
        input_value = float(label)
        item_range = cls.WRITING_VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def get_writing_user_store_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_writing_store_label())

        return positions

    @classmethod
    def get_writing_user_view_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_writing_view_label())

        return positions

    @classmethod
    def compare_writing_labels(cls, label1, label2):
        if float(label1) >= float(label2):
            return label1
        return label2

    @classmethod
    def get_writing__store_label_rank(cls, label):
        return float(label)

    #################################
    # Quantitative and Verbal methods
    #################################
    def get_q_and_v_store_label(self):
        item_range = self.Q_AND_V_STORE_LABEL_RANGE
        return str(floor((self.quantitative + self.verbal) / item_range) * item_range)

    def get_q_and_v_view_label(self):
        item_range = self.Q_AND_V_VIEW_LABEL_RANGE
        value = floor((self.quantitative + self.verbal) / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def convert_q_and_v_store_to_view_label(cls, label):
        input_value = int(label)
        item_range = cls.Q_AND_V_VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def get_q_and_v_user_store_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_q_and_v_store_label())

        return positions

    @classmethod
    def get_q_and_v_user_view_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_q_and_v_view_label())

        return positions

    @classmethod
    def compare_q_and_v_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2

    @classmethod
    def get_q_and_v__store_label_rank(cls, label):
        return float(label)


class GRESubjectCertificate(LanguageCertificate):
    quantitative = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(130), MaxValueValidator(170)],
    )
    verbal = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(130), MaxValueValidator(170)],
    )
    analytical_writing = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
    )

    total = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(200), MaxValueValidator(990), ten_factor_validator],
    )

    def clean(self, *args, **kwargs):
        if self.certificate_type not in [LanguageCertificate.LanguageCertificateType.GRE_CHEMISTRY,
                                         LanguageCertificate.LanguageCertificateType.GRE_LITERATURE,
                                         LanguageCertificate.LanguageCertificateType.GRE_MATHEMATICS]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})

    TOTAL_STORE_LABEL_RANGE = 20
    TOTAL_VIEW_LABEL_RANGE = 100

    def get_total_store_label(self):
        item_range = self.TOTAL_STORE_LABEL_RANGE
        return str(floor(self.total / item_range) * item_range)

    def get_total_view_label(self):
        item_range = self.TOTAL_VIEW_LABEL_RANGE
        value = floor(self.total / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def convert_total_store_to_view_label(cls, label):
        input_value = float(label)
        item_range = cls.TOTAL_VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def compare_total_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2

    @classmethod
    def get_total_user_store_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_total_store_label())

        return positions

    @classmethod
    def get_total_user_view_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_total_view_label())

        return positions

    @classmethod
    def get_total__store_label_rank(cls, label):
        return float(label)


class GREBiologyCertificate(GRESubjectCertificate):
    cellular_and_molecular = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    organismal = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    ecology_and_evolution = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    def clean(self, *args, **kwargs):
        if self.certificate_type not in [LanguageCertificate.LanguageCertificateType.GRE_BIOLOGY]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})


class GREPhysicsCertificate(GRESubjectCertificate):
    classical_mechanics = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    electromagnetism = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    quantum_mechanics = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    def clean(self, *args, **kwargs):
        if self.certificate_type not in [LanguageCertificate.LanguageCertificateType.GRE_PHYSICS]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})


class GREPsychologyCertificate(GRESubjectCertificate):
    biological = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    cognitive = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    social = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    developmental = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    clinical = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    measurement_or_methodology = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(99)]
    )

    def clean(self, *args, **kwargs):
        if self.certificate_type not in [LanguageCertificate.LanguageCertificateType.GRE_PSYCHOLOGY]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})


class DuolingoCertificate(LanguageCertificate):
    overall = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(160)]
    )

    literacy = models.PositiveSmallIntegerField()

    comprehension = models.PositiveSmallIntegerField()

    conversation = models.PositiveSmallIntegerField()

    production = models.PositiveSmallIntegerField()

    def clean(self, *args, **kwargs):
        if self.certificate_type not in [LanguageCertificate.LanguageCertificateType.DUOLINGO]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})

    OVERALL_STORE_LABEL_RANGE = 15
    OVERALL_VIEW_LABEL_RANGE = 30

    def get_store_label(self):
        item_range = self.OVERALL_STORE_LABEL_RANGE
        return str(floor(self.overall / item_range) * item_range + 10)

    def get_view_label(self):
        item_range = self.OVERALL_VIEW_LABEL_RANGE
        value = floor(self.overall / item_range) * item_range + 10
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def convert_store_to_view_label(cls, label):
        input_value = int(label)
        item_range = cls.OVERALL_VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + '-' + str(value + item_range)

    @classmethod
    def get__user_store_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)
        for obj in user_toefl_certificates:
            positions.append(obj.get_store_label())

        return positions

    @classmethod
    def get__user_view_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(content_type=SDI_CT, object_id=sdi.id)
        for obj in user_toefl_certificates:
            positions.append(obj.get_view_label())

        return positions

    @classmethod
    def compare_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2

    @classmethod
    def get_store_label_rank(cls, label):
        return float(label)
