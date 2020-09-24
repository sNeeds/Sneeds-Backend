import datetime
from math import ceil, floor
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from enumfields import Enum, EnumField

from .managers import UniversityThroughQuerySetManager, LanguageCertificateQuerysetManager, CountryManager
from .validators import validate_resume_file_extension, validate_resume_file_size, ten_factor_validator
from . import validators

from sNeeds.utils.custom.custom_functions import add_this_arg

MISSING_LABEL = 'missing'
REWARDED_LABEL = 'rewarded'

ZERO_LABEL = '0'

User = get_user_model()

SEMESTER_CHOICES = [
    ('spring', 'بهار'),
    ('summer', 'تابستان'),
    ('fall', 'پاییز‍'),
    ('winter', 'زمستان'),
]


class Grade(Enum):
    BACHELOR = 'کارشناسی'
    MASTER = 'ارشد'
    PHD = 'دکتری'
    POST_DOC = 'پست دکتری'


class PublicationType(Enum):
    JOURNAL = 'ژورنالی'
    CONFERENCE = 'کنفرانسی'


class LanguageCertificateType(Enum):
    IELTS_GENERAL = 'IELTS General'
    IELTS_ACADEMIC = 'IELTS Academic'
    TOEFL = 'TOEFL'
    GMAT = 'GMAT'
    GRE_GENERAL = 'GRE General'
    GRE_CHEMISTRY = 'GRE Chemistry'
    GRE_MATHEMATICS = 'GRE Mathematics'
    GRE_LITERATURE = 'GRE Literature'
    GRE_BIOLOGY = 'GRE Biology'
    GRE_PHYSICS = 'GRE Physics'
    GRE_PSYCHOLOGY = 'GRE Psychology'
    DUOLINGO = 'Duolingo'


class PaymentAffordability(Enum):
    LOW = 'کم'
    MIDDLE = 'متوسط'
    MUCH = 'زیاد'


class Gender(Enum):
    MALE = 'آقا'
    FEMALE = 'خانم'


class MilitaryServiceStatus(Enum):
    PASSED = 'گذرانده شده'
    UNDID = 'گذرانده نشده'


class WhichAuthor(Enum):
    FIRST = 'نویسنده اول'
    SECOND = 'نویسنده دوم'
    THIRD = 'نویسنده سوم'
    FOURTH_OR_MORE = 'نویسنده چهارم به بعد'


class JournalReputation(Enum):
    ONE_TO_THREE = 'از یک تا سه'
    FOUR_TO_TEN = 'از چهار تا ده'
    ABOVE_TEN = 'بیشتر از ده'


def current_year():
    return datetime.date.today().year


def get_image_upload_path(sub_dir):
    return "account/images/" + sub_dir


def get_student_resume_path(instance, filename):
    return "account/files/form/{}/resume/{}".format(instance.id, filename)


class BasicFormField(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=256, unique=True)
    search_name = models.CharField(max_length=256, unique=True)
    picture = models.ImageField(upload_to=get_image_upload_path("country-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    objects = CountryManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=256, unique=True)
    search_name = models.CharField(max_length=1024, unique=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(null=True, blank=True, upload_to=get_image_upload_path("university-pictures"))
    rank = models.PositiveIntegerField(blank=True, null=True)
    is_college = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class FieldOfStudyType(BasicFormField):
    pass


class GradeModel(BasicFormField):
    pass


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=256, unique=True)
    search_name = models.CharField(max_length=1024, unique=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(
        blank=False,
        null=True,
        upload_to=get_image_upload_path("field-of-study-pictures")
    )
    major_type = models.ForeignKey(
        FieldOfStudyType,
        null=True,
        blank=False,
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ["major_type"]

    def __str__(self):
        self.name = self.name
        return self.name


class StudentFormApplySemesterYear(models.Model):
    year = models.SmallIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        help_text="In Gregorian"
    )
    semester = models.CharField(max_length=64, choices=SEMESTER_CHOICES)

    class Meta:
        ordering = ["year", "semester"]

    def __str__(self):
        return str(self.year) + " " + self.semester


class WantToApply(models.Model):
    student_detailed_info = models.OneToOneField(
        'StudentDetailedInfo',
        on_delete=models.CASCADE,
        related_name="want_to_apply"
    )
    countries = models.ManyToManyField(
        Country,
    )

    universities = models.ManyToManyField(University)

    grades = models.ManyToManyField(
        GradeModel
    )

    majors = models.ManyToManyField(
        FieldOfStudy,
    )

    semester_years = models.ManyToManyField(
        StudentFormApplySemesterYear,
    )


class Publication(models.Model):
    student_detailed_info = models.ForeignKey(
        'StudentDetailedInfoBase',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=512)
    publish_year = models.SmallIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        help_text="In Gregorian"
    )
    which_author = EnumField(WhichAuthor, max_length=128, default=WhichAuthor.FIRST)
    type = EnumField(PublicationType, max_length=20, default=PublicationType.JOURNAL)

    journal_reputation = EnumField(
        JournalReputation,
        max_length=128,
        null=True,
    )

    value = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        editable=False
    )  # Updated in signal

    PUBLICATIONS_SCORE__STORE_LABEL_RANGE = 0.5
    PUBLICATIONS_SCORE__VIEW_LABEL_RANGE = 1

    def __str__(self):
        return self.title

    def get_count_chart__store_label(self):
        return str(self.student_detailed_info.publication_set.count())

    def get_type__store_label(self):
        return self.type.name

    def get_impact_factor__store_label(self):
        return self.journal_reputation.name

    @classmethod
    def get_publications_score__store_label(cls, value):
        item_range = cls.PUBLICATIONS_SCORE__STORE_LABEL_RANGE
        return str(floor(value / item_range) * item_range)

    def get_type__view_label(self):
        return self.type.name

    def get_impact_factor__view_label(self):
        return self.journal_reputation.name

    @classmethod
    def get_publications_score__view_label(cls, input_value):
        if input_value >= 4:
            return '+4'
        item_range = cls.PUBLICATIONS_SCORE__VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def convert_publications_score__store_to_view_label(cls, label):
        input_value = float(label)
        item_range = cls.PUBLICATIONS_SCORE__VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def convert_count_chart_store_to_view_label(cls, label):
        count = int(label)
        if count < 3:
            return label
        if count >= 4:
            return '+4'

    @classmethod
    def get_publication_count_user_store_based_positions(cls, sdi):
        return [str(cls.objects.filter(student_detailed_info=sdi).count())]

    @classmethod
    def get_publication_count_user_view_based_positions(cls, sdi):
        return [cls.convert_count_chart_store_to_view_label(str(cls.objects.filter(student_detailed_info=sdi).count()))]

    @classmethod
    def get_publication_type_user_store_based_positions(cls, sdi):
        qs = cls.objects.filter(student_detailed_info=sdi)
        positions = []

        for obj in qs:
            positions.append(obj.get_type__store_label())
        return positions

    @classmethod
    def get_publication_type_user_view_based_positions(cls, sdi):
        qs = cls.objects.filter(student_detailed_info=sdi)
        positions = []

        for obj in qs:
            positions.append(obj.get_type__view_label())
        return positions

    @classmethod
    def get_publications_score_user_store_based_positions(cls, sdi):
        qs = cls.objects.filter(student_detailed_info=sdi)
        positions = []

        for obj in qs:
            positions.append(obj.value)
        return positions

    @classmethod
    def get_publications_score_user_view_based_positions(cls, sdi):
        qs = cls.objects.filter(student_detailed_info=sdi)
        positions = []

        for obj in qs:
            positions.append(obj.value)
        return positions

    @classmethod
    def get_publication_impact_factor_user_store_based_positions(cls, sdi):
        qs = cls.objects.filter(student_detailed_info=sdi)
        positions = []

        for obj in qs:
            positions.append(obj.get_impact_factor__store_label())
        return positions

    @classmethod
    def get_publication_impact_factor_user_view_based_positions(cls, sdi):
        qs = cls.objects.filter(student_detailed_info=sdi)
        positions = []

        for obj in qs:
            positions.append(obj.get_impact_factor__view_label())
        return positions

    @classmethod
    def compare_publication_count_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2

    @classmethod
    def compare_publications_score_labels(cls, label1, label2):
        if float(label1) >= float(label2):
            return label1
        return label2

    @classmethod
    def compare_publication_impact_factor_labels(cls, label1, label2):
        if (label1 == JournalReputation.ONE_TO_THREE) or \
                (label1 == JournalReputation.FOUR_TO_TEN and label2 == JournalReputation.ABOVE_TEN):
            return label1

        elif (label1 == JournalReputation.ABOVE_TEN) or \
                (label1 == JournalReputation.FOUR_TO_TEN and label2 == JournalReputation.ONE_TO_THREE):
            return label2
        return label1


class StudentDetailedInfoBase(models.Model):
    id = models.UUIDField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    universities = models.ManyToManyField(
        University,
        through='UniversityThrough'
    )

    resume = models.FileField(
        upload_to=get_student_resume_path,
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']), validate_resume_file_size
        ]
    )
    related_work_experience = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="In months"
    )
    academic_break = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="In years"
    )
    olympiad = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class StudentDetailedInfo(StudentDetailedInfoBase):
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(15), MaxValueValidator(100)],
        null=True,
        blank=True,
    )

    gender = EnumField(
        Gender,
        default=Gender.MALE,
        null=True,
        blank=True,
    )

    military_service_status = EnumField(
        MilitaryServiceStatus,
        default=MilitaryServiceStatus.UNDID,
        max_length=30,
        null=True,
        blank=True,
    )

    is_married = models.BooleanField(
        default=None,
        null=True,
        blank=True
    )

    payment_affordability = EnumField(
        PaymentAffordability,
        default=PaymentAffordability.MIDDLE,
        max_length=30,
        null=True,
        blank=True,
    )

    prefers_full_fund = models.BooleanField(
        default=None,
        null=True,
        blank=True
    )
    prefers_half_fund = models.BooleanField(
        default=None,
        null=True,
        blank=True
    )
    prefers_self_fund = models.BooleanField(
        default=None,
        null=True,
        blank=True
    )

    # Extra info
    comment = models.TextField(max_length=1024, null=True, blank=True)
    powerful_recommendation = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )
    linkedin_url = models.URLField(
        blank=True,
        null=True,
    )
    homepage_url = models.URLField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['created', ]

    RELATED_WORK_EXPERIENCE_STORE_LABEL_RANGE = 2
    RELATED_WORK_EXPERIENCE_VIEW_LABEL_RANGE = 6

    def is_complete(self):
        return True

    def get_related_majors(self):
        related_majors = FieldOfStudy.objects.none()

        university_through_qs = UniversityThrough.objects.filter(
            student_detailed_info__id=self.id
        )
        related_majors |= university_through_qs.values_list('major', flat=True)

        try:
            want_to_apply = WantToApply.objects.get(student_detailed_info__id=self.id)
            related_majors |= want_to_apply.majors.all()
        except WantToApply.DoesNotExist:
            pass

        return related_majors

    def get_powerful_recommendation__store_label(self):
        return MISSING_LABEL if not self.powerful_recommendation or self.powerful_recommendation is None\
            else REWARDED_LABEL

    def get_olympiad__store_label(self):
        return MISSING_LABEL if self.olympiad is None or len(self.olympiad) == 0 else REWARDED_LABEL

    def get_related_work__store_label(self):
        if self.related_work_experience is None:
            return '0'
        item_range = self.RELATED_WORK_EXPERIENCE_STORE_LABEL_RANGE
        return str(floor(self.related_work_experience / item_range) * item_range)

    def get_powerful_recommendation__view_label(self):
        return REWARDED_LABEL if self.powerful_recommendation else MISSING_LABEL

    def get_olympiad__view_label(self):
        return MISSING_LABEL if self.olympiad is None or len(self.olympiad) == 0 else REWARDED_LABEL

    def get_related_work__view_label(self):
        if self.related_work_experience >= 36:
            return '+36'
        item_range = self.RELATED_WORK_EXPERIENCE_VIEW_LABEL_RANGE
        value = floor(self.related_work_experience / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def convert_related_work_store_to_view_label(cls, label):
        input_value = int(label)
        if input_value >= 36:
            return '+36'
        item_range = cls.RELATED_WORK_EXPERIENCE_VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def compare_powerful_recommendation_labels(cls, label1, label2):
        if label1 == label2 or label1 == REWARDED_LABEL:
            return label1
        return label2

    @classmethod
    def compare_olympiad_labels(cls, label1, label2):
        if label1 == label2 or label1 == REWARDED_LABEL:
            return label1
        return label2

    @classmethod
    def compare_related_work_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2


class UniversityThrough(models.Model):
    university = models.ForeignKey(
        University, on_delete=models.PROTECT
    )
    student_detailed_info = models.ForeignKey(
        StudentDetailedInfoBase,
        on_delete=models.CASCADE
    )
    grade = EnumField(Grade, default=Grade.BACHELOR)
    major = models.ForeignKey(
        FieldOfStudy, on_delete=models.PROTECT
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
    objects = UniversityThroughQuerySetManager.as_manager()

    class Meta:
        unique_together = ['student_detailed_info', 'grade']

    GPA_STORE_LABEL_RANGE = 0.25
    GPA_VIEW_LABEL_RANGE = 1

    def get_gpa__store_label(self):
        item_range = self.GPA_STORE_LABEL_RANGE
        return str(floor(self.gpa / item_range) * item_range)

    def get_gpa__view_label(self):
        if self.gpa < 12:
            return '-12'
        item_range = self.GPA_VIEW_LABEL_RANGE
        value = floor(self.gpa / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def convert_gpa_store_to_view_label(cls, label):
        input_value = int(label)
        if input_value < 12:
            return '-12'
        item_range = cls.GPA_VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def get_gpa_user_store_based_positions(cls, sdi):
        user_last_grade = cls.objects.filter(student_detailed_info=sdi) \
            .order_by('-graduate_in').first()
        if user_last_grade is None:
            return None
        return [user_last_grade.get_gpa__store_label()]

    @classmethod
    def get_gpa_user_view_based_positions(cls, sdi):
        user_last_grade = cls.objects.filter(student_detailed_info=sdi) \
            .order_by('-graduate_in').first()
        if user_last_grade is None:
            return None
        return [user_last_grade.get_gpa__view_label()]

    @classmethod
    def compare_gpa_labels(cls, label1, label2):
        if float(label1) >= float(label2):
            return label1
        return label2


class LanguageCertificate(models.Model):
    certificate_type = EnumField(
        LanguageCertificateType,
        default=LanguageCertificateType.TOEFL,
        max_length=64,
        help_text="Based on endpoint just some types are allowed to insert not all certificate types."
    )
    student_detailed_info = models.ForeignKey(
        StudentDetailedInfoBase,
        on_delete=models.CASCADE
    )
    is_mock = models.BooleanField(
        default=False
    )

    objects = LanguageCertificateQuerysetManager.as_manager()

    class Meta:
        unique_together = ('certificate_type', 'student_detailed_info')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class RegularLanguageCertificate(LanguageCertificate):
    speaking = models.DecimalField(max_digits=5, decimal_places=2)
    listening = models.DecimalField(max_digits=5, decimal_places=2)
    writing = models.DecimalField(max_digits=5, decimal_places=2)
    reading = models.DecimalField(max_digits=5, decimal_places=2)
    overall = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self, *args, **kwargs):
        if self.certificate_type not in [LanguageCertificateType.IELTS_ACADEMIC, LanguageCertificateType.IELTS_GENERAL,
                                         LanguageCertificateType.TOEFL]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})

    IELTS__STORE_LABEL_RANGE = 0.5
    IELTS__VIEW_LABEL_RANGE = 1
    TOEFL__STORE_LABEL_RANGE = 10
    TOEFL__VIEW_LABEL_RANGE = 20

    def get_ielts__store_label(self):
        item_range = self.IELTS__STORE_LABEL_RANGE
        return str(floor(self.overall / item_range) * item_range)

    def get_toefl__store_label(self):
        item_range = self.TOEFL__STORE_LABEL_RANGE
        return str(floor(self.overall / item_range) * item_range)

    def get_ielts__view_label(self):
        item_range = self.IELTS__VIEW_LABEL_RANGE
        return str(floor(self.overall / item_range) * item_range)

    def get_toefl__view_label(self):
        item_range = self.TOEFL__VIEW_LABEL_RANGE
        return str(floor(self.overall / item_range) * item_range)

    @classmethod
    def convert_ielts_store_to_view_label(cls, label):
        value = int(label)
        item_range = cls.IELTS__VIEW_LABEL_RANGE
        return str(floor(value / item_range) * item_range)

    @classmethod
    def convert_toefl_store_to_view_label(cls, label):
        value = int(label)
        item_range = cls.TOEFL__VIEW_LABEL_RANGE
        return str(floor(value / item_range) * item_range)

    @classmethod
    def get_toefl_user_store_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(student_detailed_info=sdi,
                                                     certificate_type=LanguageCertificateType.TOEFL
                                                     )
        for obj in user_toefl_certificates:
            positions.append(obj.get_toefl__store_label())

        return positions

    @classmethod
    def get_toefl_user_view_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(student_detailed_info=sdi,
                                                     certificate_type=LanguageCertificateType.TOEFL
                                                     )
        for obj in user_toefl_certificates:
            positions.append(obj.get_toefl__view_label())

        return positions

    @classmethod
    def get_ielts_user_store_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(Q(student_detailed_info=sdi) and
                                                     (Q(certificate_type=LanguageCertificateType.IELTS_GENERAL) or
                                                      Q(certificate_type=LanguageCertificateType.IELTS_ACADEMIC))
                                                     )

        for obj in user_toefl_certificates:
            positions.append(obj.get_ielts__store_label())

        return positions

    @classmethod
    def get_ielts_user_view_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(Q(student_detailed_info=sdi) and
                                                     (Q(certificate_type=LanguageCertificateType.IELTS_GENERAL) or
                                                      Q(certificate_type=LanguageCertificateType.IELTS_ACADEMIC))
                                                     )

        for obj in user_toefl_certificates:
            positions.append(obj.get_ielts__view_label())

        return positions

    @classmethod
    def compare_ielts_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2

    @classmethod
    def compare_toefl_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2


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
        if self.certificate_type not in [LanguageCertificateType.GMAT]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})

    def get_store_label(self):
        item_range = self.TOTAL_STORE_LABEL_RANGE
        return str(floor(self.total / item_range) * item_range)

    def get_view_label(self):
        item_range = self.TOTAL_VIEW_LABEL_RANGE
        return str(floor(self.total / item_range) * item_range)

    @classmethod
    def convert_store_to_view_label(cls, label):
        value = int(label)
        item_range = cls.TOTAL_VIEW_LABEL_RANGE
        return str(floor(value / item_range) * item_range)

    @classmethod
    def get_user_store_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(student_detailed_info=sdi)
        for obj in user_toefl_certificates:
            positions.append(obj.get_store_label())

        return positions

    @classmethod
    def get_user_view_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(student_detailed_info=sdi)
        for obj in user_toefl_certificates:
            positions.append(obj.get_view_label())

        return positions

    @classmethod
    def compare_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2


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
        if self.certificate_type not in [LanguageCertificateType.GRE_GENERAL]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})

    WRITING_STORE_LABEL_RANGE = 0.5
    WRITING_VIEW_LABEL_RANGE = 10
    Q_AND_V_STORE_LABEL_RANGE = 0.5
    Q_AND_V_VIEW_LABEL_RANGE = 20

    def get_writing_store_label(self):
        item_range = self.WRITING_STORE_LABEL_RANGE
        return str(floor(self.analytical_writing / item_range) * item_range)

    def get_q_and_v_store_label(self):
        item_range = self.Q_AND_V_STORE_LABEL_RANGE
        return str(floor((self.quantitative + self.verbal) / item_range) * item_range)

    def get_writing_view_label(self):
        item_range = self.WRITING_VIEW_LABEL_RANGE
        return str(floor(self.analytical_writing / item_range) * item_range)

    def get_q_and_v_view_label(self):
        item_range = self.Q_AND_V_VIEW_LABEL_RANGE
        return str(floor((self.quantitative + self.verbal) / item_range) * item_range)

    @classmethod
    def convert_writing_store_to_view_label(cls, label):
        value = float(label)
        item_range = cls.WRITING_VIEW_LABEL_RANGE
        return str(floor(value / item_range) * item_range)

    @classmethod
    def convert_q_and_v_store_to_view_label(cls, label):
        value = int(label)
        item_range = cls.Q_AND_V_VIEW_LABEL_RANGE
        return str(floor(value / item_range) * item_range)

    @classmethod
    def get_writing_user_store_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(student_detailed_info=sdi)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_writing_store_label())

        return positions

    @classmethod
    def get_writing_user_view_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(student_detailed_info=sdi)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_writing_view_label())

        return positions

    @classmethod
    def get_q_and_v_user_store_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(student_detailed_info=sdi)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_q_and_v_store_label())

        return positions

    @classmethod
    def get_q_and_v_user_view_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(student_detailed_info=sdi)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_q_and_v_view_label())

        return positions

    @classmethod
    def compare_writing_labels(cls, label1, label2):
        if float(label1) >= float(label2):
            return label1
        return label2

    @classmethod
    def compare_q_and_v_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2


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
        if self.certificate_type not in [LanguageCertificateType.GRE_CHEMISTRY, LanguageCertificateType.GRE_LITERATURE,
                                         LanguageCertificateType.GRE_MATHEMATICS]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})

    TOTAL_STORE_LABEL_RANGE = 20
    TOTAL_VIEW_LABEL_RANGE = 100

    def get_total_store_label(self):
        item_range = self.TOTAL_STORE_LABEL_RANGE
        return str(floor(self.total / item_range) * item_range)

    def get_total_view_label(self):
        item_range = self.TOTAL_VIEW_LABEL_RANGE
        return str(floor(self.total / item_range) * item_range)

    @classmethod
    def convert_total_store_to_view_label(cls, label):
        value = float(label)
        item_range = cls.TOTAL_VIEW_LABEL_RANGE
        return str(floor(value / item_range) * item_range)

    @classmethod
    def compare_total_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2

    @classmethod
    def get_total_user_store_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(student_detailed_info=sdi)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_total_store_label())

        return positions

    @classmethod
    def get_total_user_view_based_positions(cls, sdi):
        positions = []
        user_gre_general_certificates = cls.objects.filter(student_detailed_info=sdi)

        for obj in user_gre_general_certificates:
            positions.append(obj.get_total_view_label())

        return positions


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
        if self.certificate_type not in [LanguageCertificateType.GRE_BIOLOGY]:
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
        if self.certificate_type not in [LanguageCertificateType.GRE_PHYSICS]:
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
        if self.certificate_type not in [LanguageCertificateType.GRE_PSYCHOLOGY]:
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
        if self.certificate_type not in [LanguageCertificateType.DUOLINGO]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})

    OVERALL_STORE_LABEL_RANGE = 15
    OVERALL_VIEW_LABEL_RANGE = 30

    def get_store_label(self):
        item_range = self.OVERALL_STORE_LABEL_RANGE
        return str(floor(self.overall / item_range) * item_range)

    def get_view_label(self):
        item_range = self.OVERALL_VIEW_LABEL_RANGE
        return str(floor(self.overall / item_range) * item_range)

    @classmethod
    def convert_store_to_view_label(cls, label):
        value = int(label)
        item_range = cls.OVERALL_VIEW_LABEL_RANGE
        return str(floor(value / item_range) * item_range)

    @classmethod
    def get__user_store_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(student_detailed_info=sdi)
        for obj in user_toefl_certificates:
            positions.append(obj.get_store_label())

        return positions

    @classmethod
    def get__user_view_based_positions(cls, sdi):
        positions = []
        user_toefl_certificates = cls.objects.filter(student_detailed_info=sdi)
        for obj in user_toefl_certificates:
            positions.append(obj.get_view_label())

        return positions

    @classmethod
    def compare_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2
