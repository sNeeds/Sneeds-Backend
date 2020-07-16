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
    ('بهار', 'بهار'),
    ('تابستان', 'تابستان'),
    ('پاییز', 'پاییز‍'),
    ('زمستان', 'زمستان'),
]

# Attention the names must be the same as the field names in the model
STUDENT_FORM_CATEGORY_CHOICES = [
    ('marital_status', 'marital_status'),
    ('publication_type', 'publication_type'),
    ('university_major_type', 'university_major_type'),
    ('want_to_apply_major_type', 'want_to_apply_major_type'),
    ('payment_affordability', 'payment_affordability'),
    ('publication_which_author', 'publication_which_author')
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


class StudentFormFieldsChoice(models.Model):
    name = models.CharField(max_length=256)
    category = models.CharField(
        max_length=256,
        choices=STUDENT_FORM_CATEGORY_CHOICES
    )

    class Meta:
        ordering = ["category", "name"]
        unique_together = ["category", "name"]

    def __str__(self):
        return self.name


class StudentFormApplySemesterYear(models.Model):
    year = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text="In Gregorian"
    )
    semester = models.CharField(max_length=64, choices=SEMESTER_CHOICES)

    class Meta:
        ordering = ["year", "semester"]

    def __str__(self):
        return str(self.year) + " " + self.semester


class FormUniversity(models.Model):
    name = models.CharField(max_length=128)
    value = models.IntegerField()


class FormGrade(models.Model):
    name = models.CharField(max_length=128)


class FormMajor(models.Model):
    name = models.CharField(max_length=128)


class FormMajorType(models.Model):
    name = models.CharField(max_length=128)


class LanguageCertificateType(models.Model):
    name = models.CharField(
        max_length=128
    )


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


class PublicationType(models.Model):
    student_form_fields_choice = models.ForeignKey(
        StudentFormFieldsChoice,
        on_delete=models.PROTECT,
        related_name='publication_type'
    )
    value = models.IntegerField()

    def clean(self):
        if self.student_form_fields_choice.category != "publication_type":
            raise ValidationError(
                {
                    "student_form_fields_choice": "StudentFormFieldsChoice type is not publication_type"
                }
            )


class Publication(models.Model):
    title = models.CharField(max_length=512)
    publish_year = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text="In Gregorian"
    )
    which_author = models.ForeignKey(
        StudentFormFieldsChoice,
        on_delete=models.PROTECT,
        related_name='publication_which_author'
    )
    type = models.ForeignKey(
        PublicationType,
        on_delete=models.PROTECT
    )


class StudentDetailedInfo(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(15), MaxValueValidator(100)]
    )

    marital_status = models.ForeignKey(
        StudentFormFieldsChoice,
        on_delete=models.PROTECT,
        related_name='marital_status'
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
        StudentFormFieldsChoice,
        on_delete=models.PROTECT,
        related_name='payment_affordability'
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
        validators=[MinValueValidator(0), MaxValueValidator(100)]
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
    major_type = models.ForeignKey(
        StudentFormFieldsChoice,
        on_delete=models.PROTECT,
        related_name='university_major_type'
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
    major_type = models.ForeignKey(
        StudentFormFieldsChoice,
        on_delete=models.PROTECT,
        related_name='want_to_apply_major_type'
    )
    major = models.CharField(
        max_length=256
    )
