import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
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
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to=get_image_upload_path("university-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to=get_image_upload_path("field-of-study-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    class Meta:
        ordering = ["name"]

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


class BasicFormField(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class FormUniversity(BasicFormField):
    value = models.IntegerField()
    is_college = models.BooleanField(default=False)


class FormGrade(BasicFormField):
    pass


class FormMajorType(BasicFormField):
    pass


class FormMajor(BasicFormField):
    major_type = models.ForeignKey(
        FormMajorType,
        on_delete=models.PROTECT,
    )


class LanguageCertificateType(BasicFormField):
    pass


class WantToApply(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT
    )

    universities = models.ManyToManyField(
        University,
        through='UniversityWantToApplyThrough'
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
        on_delete=models.CASCADE
    )

    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(15), MaxValueValidator(100)]
    )

    marital_status = models.ForeignKey(
        MaritalStatus,
        on_delete=models.PROTECT,
    )

    universities = models.ManyToManyField(
        FormUniversity,
        through='FormUniversityThrough'
    )

    language_certificates = models.ManyToManyField(
        LanguageCertificateType,
        through='LanguageCertificateTypeThrough'
    )

    want_to_apply = models.ManyToManyField(
        WantToApply,
    )

    publications = models.ManyToManyField(
        Publication
    )

    payment_affordability = models.ForeignKey(
        PaymentAffordability,
        on_delete=models.PROTECT,
    )

    prefers_full_fund = models.BooleanField(default=False)
    prefers_half_fund = models.BooleanField(default=False)
    prefers_self_fund = models.BooleanField(default=False)

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
        default=False
    )
    linkedin_url = models.URLField(
        blank=True,
        null=True
    )
    homepage_url = models.URLField(
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_complete(self):
        return True


class FormUniversityThrough(models.Model):
    university = models.ForeignKey(
        FormUniversity, on_delete=models.PROTECT
    )
    student_detailed_info = models.ForeignKey(
        StudentDetailedInfo,
        on_delete=models.CASCADE
    )
    grade = models.ForeignKey(
        FormGrade, on_delete=models.PROTECT
    )
    major = models.ForeignKey(
        FormMajor, on_delete=models.PROTECT
    )
    graduate_in = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
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


class UniversityWantToApplyThrough(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.PROTECT
    )
    want_to_apply = models.ForeignKey(
        WantToApply,
        on_delete=models.CASCADE
    )
    grade = models.ForeignKey(
        FormGrade,
        on_delete=models.PROTECT
    )

    major = models.ForeignKey(
        FormMajor,
        on_delete=models.PROTECT
    )
