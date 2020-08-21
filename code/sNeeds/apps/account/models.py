import datetime
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from enumfields import Enum, EnumField

from .managers import UniversityThroughQuerySetManager, LanguageCertificateQuerysetManager
from .validators import validate_resume_file_extension, validate_resume_file_size, ten_factor_validator
from . import validators

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
    picture = models.ImageField(upload_to=get_image_upload_path("country-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=256, unique=True)
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
    student_detailed_info = models.ForeignKey(
        'StudentDetailedInfoBase',
        on_delete=models.CASCADE
    )
    countries = models.ManyToManyField(
        Country,
    )

    universities = models.ManyToManyField(University)

    # grades = EnumField(Grade, default=Grade.BACHELOR)
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

    def __str__(self):
        return self.title


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

    def is_complete(self):
        return True

    class Meta:
        ordering = ['created', ]


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

    def clean(self, *args, **kwargs):
        if self.certificate_type not in [LanguageCertificateType.GMAT]:
            raise ValidationError({'certificate_type': _("Value is not in allowed certificate types.")})


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
