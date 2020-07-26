import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


from .validators import validate_resume_file_extension, validate_resume_file_size

from . import validators

User = get_user_model()

SEMESTER_CHOICES = [
    ('spring', 'بهار'),
    ('summer', 'تابستان'),
    ('fall', 'پاییز‍'),
    ('winter', 'زمستان'),
]


def current_year():
    return datetime.date.today().year


def get_image_upload_path(sub_dir):
    return "account/images/" + sub_dir


def get_student_resume_path(instance, filename):
    return "account/files/students/{}/resume/{}".format(instance.user.email, filename)


class BasicFormField(models.Model):
    name = models.CharField(max_length=256)
    name_search = SearchVectorField(null=True)

    class Meta:
        indexes = [GinIndex(fields=["name_search"])]

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


class FormGrade(BasicFormField):
    pass


class LanguageCertificateType(BasicFormField):
    pass


class GMATCertificate(models.Model):
    student_detailed_info = models.ForeignKey(
        'StudentDetailedInfo',
        on_delete=models.CASCADE,
    )
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


class GRECertificate(models.Model):
    student_detailed_info = models.ForeignKey(
        'StudentDetailedInfo',
        on_delete=models.CASCADE,
    )
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


class WantToApply(models.Model):
    student_detailed_info = models.ForeignKey(
        'StudentDetailedInfo',
        on_delete=models.CASCADE
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT
    )

    university = models.ForeignKey(
        University,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    grade = models.ForeignKey(
        FormGrade,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    major = models.ForeignKey(
        FieldOfStudy,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    semester_year = models.ForeignKey(
        StudentFormApplySemesterYear,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return str(self.country)


class PublicationType(BasicFormField):
    value = models.IntegerField()


class PublicationWhichAuthor(BasicFormField):
    value = models.IntegerField()


class Publication(models.Model):
    student_detailed_info = models.ForeignKey(
        'StudentDetailedInfo',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=512)
    publish_year = models.SmallIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        help_text="In Gregorian"
    )
    which_author = models.ForeignKey(
        PublicationWhichAuthor,
        on_delete=models.PROTECT,
    )
    type = models.ForeignKey(
        PublicationType,
        on_delete=models.PROTECT
    )

    # impact_factor

    def __str__(self):
        return self.title


class PaymentAffordability(BasicFormField):
    value = models.IntegerField()


class MaritalStatus(BasicFormField):
    pass


class StudentDetailedInfo(models.Model):
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

    # gender = models.BooleanField(
    #     null=True,
    #     blank=True,
    # )

    # passed_military_service = models.BooleanField(
    #     null=True,
    #     blank=True
    # )

    marital_status = models.ForeignKey(
        MaritalStatus,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    universities = models.ManyToManyField(
        University,
        through='UniversityThrough'
    )

    language_certificates = models.ManyToManyField(
        LanguageCertificateType,
        through='LanguageCertificateTypeThrough'
    )

    payment_affordability = models.ForeignKey(
        PaymentAffordability,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    prefers_full_fund = models.BooleanField(default=False,
                                            null=True,
                                            blank=True, )
    prefers_half_fund = models.BooleanField(default=False,
                                            null=True,
                                            blank=True, )
    prefers_self_fund = models.BooleanField(default=False,
                                            null=True,
                                            blank=True,
                                            )

    # Extra info
    comment = models.TextField(max_length=1024, null=True, blank=True)
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

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_complete(self):
        return True


class UniversityThrough(models.Model):
    university = models.ForeignKey(
        University, on_delete=models.PROTECT
    )
    student_detailed_info = models.ForeignKey(
        StudentDetailedInfo,
        on_delete=models.CASCADE
    )
    grade = models.ForeignKey(
        FormGrade, on_delete=models.PROTECT
    )
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


class LanguageCertificateTypeThrough(models.Model):
    certificate_type = models.ForeignKey(
        LanguageCertificateType,
        on_delete=models.PROTECT
    )
    student_detailed_info = models.ForeignKey(
        StudentDetailedInfo,
        on_delete=models.CASCADE
    )
    speaking = models.DecimalField(max_digits=5, decimal_places=2)
    listening = models.DecimalField(max_digits=5, decimal_places=2)
    writing = models.DecimalField(max_digits=5, decimal_places=2)
    reading = models.DecimalField(max_digits=5, decimal_places=2)
    overall = models.DecimalField(max_digits=5, decimal_places=2)
