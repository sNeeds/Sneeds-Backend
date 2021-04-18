from math import floor

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models

from rest_framework.settings import api_settings
from rest_framework.exceptions import ValidationError as DRFValidationError

from abroadin.apps.data.applydata.models import Education, LanguageCertificate, Publication, Grade, SemesterYear, \
    GradeChoices
from abroadin.apps.data.applydata.values.language import LANGUAGE_B_VALUE
from abroadin.apps.estimation.form.variables import MISSING_LABEL, REWARDED_LABEL
from abroadin.apps.estimation.form.managers import StudentDetailedInfoManager, WantToApplyManager

from abroadin.apps.data.globaldata.models import (
    Country,
    University,
    Major,
    get_student_resume_path,
    User,
    BasicFormField
)

from abroadin.apps.data.applydata import models as ad_models
from abroadin.apps.data.globaldata.validators import validate_resume_file_size


def get_sdi_ct_or_none():
    try:
        return ContentType.objects.get(app_label='form', model='studentdetailedinfo')
    except ContentType.DoesNotExist:
        return None


class WantToApply(models.Model):
    student_detailed_info = models.OneToOneField(
        'StudentDetailedInfo',
        on_delete=models.CASCADE,
        related_name="want_to_apply",
    )
    countries = models.ManyToManyField(Country, blank=True)
    universities = models.ManyToManyField(University, blank=True)
    grades = models.ManyToManyField(Grade, blank=True)
    majors = models.ManyToManyField(Major, blank=True)
    semester_years = models.ManyToManyField(SemesterYear, blank=True)

    objects = WantToApplyManager.as_manager()

    @property
    def is_complete(self):
        check_fields = ['countries', 'grades']
        if not self:
            return False
        completed = True
        non_complete_fields = []
        for field in check_fields:
            if not getattr(self, field).exists():
                non_complete_fields.append(field)
                completed = False
        return completed

    def grades_want_to_apply(self):
        # TODO: VERY IMPORTANT ***************
        # Hossein change the structure of is_completed definition in WantToApply.
        # Tell me afterwards *************#########
        # **********************************************
        # **********************************************
        # **********************************************
        return self.grades.all()

    def get_countries_qs(self):
        return self.countries.all()

    def get_universities_qs(self):
        return self.universities.all()


class StudentDetailedInfo(models.Model):
    completed_credentials = [
        {'function_name': "_has_age",
         'information': {'section': 'personal', 'model': 'StudentDetailedInfo', 'fields': ['age'], 'id': 1},
         },
        {'function_name': "_has_academic_break",
         'information': {'section': 'personal', 'model': 'StudentDetailedInfo', 'fields': ['academic_break'], 'id': 2},
         },
        {'function_name': "_has_powerful_recommendation",
         'information': {'section': 'personal', 'model': 'StudentDetailedInfo', 'fields': ['powerful_recommendation'],
                         'id': 3},
         },
        {'function_name': "_has_related_work_experience",
         'information': {'section': 'personam', 'model': 'StudentDetailedInfo', 'fields': ['related_work_experience'],
                         'id': 4},
         },
        {'function_name': "_has_education",
         'information': {'section': 'academic_degree', 'model': 'Education', 'fields': [], 'id': 5},
         },
        {'function_name': "_has_completed_want_to_apply",
         'information': {'section': 'apply_destination', 'model': 'WantToApply',
                         'fields': ['countries', 'grades'], 'id': 6},
         },
    ]

    class PaymentAffordabilityChoices(models.TextChoices):
        LOW = 'Low', 'Low'
        AVERAGE = 'Average', 'Average'
        HIGH = 'High', 'High'

    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'

    publications = GenericRelation(
        Publication, related_query_name='student_detailed_info'
    )
    educations = GenericRelation(
        Education, related_query_name='student_detailed_info'
    )
    language_certificates = GenericRelation(
        LanguageCertificate, related_query_name='student_detailed_info'
    )
    regular_certificates = GenericRelation(
        ad_models.RegularLanguageCertificate, related_query_name='student_detailed_info'
    )
    gmat_certificates = GenericRelation(
        ad_models.GMATCertificate, related_query_name='student_detailed_info'
    )
    gre_general_certificates = GenericRelation(
        ad_models.GREGeneralCertificate, related_query_name='student_detailed_info'
    )
    gre_subject_certificates = GenericRelation(
        ad_models.GRESubjectCertificate, related_query_name='student_detailed_info'
    )
    gre_biology_certificates = GenericRelation(
        ad_models.GREBiologyCertificate, related_query_name='student_detailed_info'
    )
    gre_physics_certificates = GenericRelation(
        ad_models.GREPhysicsCertificate, related_query_name='student_detailed_info'
    )
    gre_psychology_certificates = GenericRelation(
        ad_models.GREPsychologyCertificate, related_query_name='student_detailed_info'
    )
    duolingo_certificates = GenericRelation(
        ad_models.DuolingoCertificate, related_query_name='student_detailed_info'
    )

    resume = models.FileField(
        null=True,
        blank=True,
        upload_to=get_student_resume_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']), validate_resume_file_size
        ]
    )

    related_work_experience = models.PositiveIntegerField(help_text="In months")
    academic_break = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="In years"
    )

    olympiad = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15), MaxValueValidator(100)])

    gender = models.CharField(max_length=128, choices=GenderChoices.choices)

    is_married = models.BooleanField(
        default=None,
        null=True,
        blank=True
    )

    payment_affordability = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        choices=PaymentAffordabilityChoices.choices,
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
    comment = models.TextField(
        max_length=1024,
        null=True,
        blank=True
    )
    powerful_recommendation = models.BooleanField()
    linkedin_url = models.URLField(
        blank=True,
        null=True,
    )
    homepage_url = models.URLField(
        blank=True,
        null=True,
    )

    value = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True
    )

    rank = models.IntegerField(
        validators=[MinValueValidator(1)],
        editable=False
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def _education_has_this_major(self, major):
        return Education.objects.filter(
            student_detailed_info__id=self.id,
            major=major
        ).exists()

    def education_has_these_majors(self, majors_list):
        found = False
        for major in majors_list:
            found = found or self._education_has_this_major(major)
        return found

    def last_education(self):
        education_qs = Education.objects.filter(content_type=get_sdi_ct_or_none(), object_id=self.id)
        return education_qs.last_education()

    def language_certificates_str(self):
        return LanguageCertificate.objects.filter(content_type=get_sdi_ct_or_none(), object_id=self.id).brief_str()

    objects = StudentDetailedInfoManager.as_manager()

    class Meta:
        ordering = ['rank', ]

    RELATED_WORK_EXPERIENCE_STORE_LABEL_RANGE = 2
    RELATED_WORK_EXPERIENCE_VIEW_LABEL_RANGE = 6

    @property
    def last_education(self):
        if not hasattr(self, '_cached_last_education'):
            self._cached_last_education = self.educations.last_education()
        return self._cached_last_education

    @property
    def bachelor_education(self):
        try:
            return self.educations.all().get(grade=GradeChoices.BACHELOR)
        except Education.DoesNotExist:
            return None
        except Education.MultipleObjectsReturned:
            return list(self.educations.all().filter(grade=GradeChoices.BACHELOR))

    @property
    def master_education(self):
        try:
            return self.educations.all().get(grade=GradeChoices.MASTER)
        except Education.DoesNotExist:
            return None
        except Education.MultipleObjectsReturned:
            return list(self.educations.all().filter(grade=GradeChoices.MASTER))

    @property
    def phd_education(self):
        try:
            return self.educations.all().get(grade=GradeChoices.PHD)
        except Education.DoesNotExist:
            return None
        except Education.MultipleObjectsReturned:
            return list(self.educations.all().filter(grade=GradeChoices.PHD))

    @property
    def post_doc_education(self):
        try:
            return self.educations.all().get(grade=GradeChoices.POST_DOC)
        except Education.DoesNotExist:
            return None
        except Education.MultipleObjectsReturned:
            return list(self.educations.all().filter(grade=GradeChoices.POST_DOC))

    def _compute_rank(self):
        better_rank_qs = self.__class__.objects.filter(value__gt=self.value)
        return better_rank_qs.count() + 1

    def _compute_value(self):
        publications = Publication.objects.filter(
            content_type=get_sdi_ct_or_none(), object_id=self.id
        )
        languages = LanguageCertificate.objects.filter(
            content_type=get_sdi_ct_or_none(), object_id=self.id
        )
        total_value = 0

        if self.last_education:
            total_value += 3.75 * self.last_education.value

        if languages.exists():
            total_value += languages.get_total_value()
        else:  # when user inputted nothing
            total_value += LANGUAGE_B_VALUE

        total_value += publications.total_value()

        total_value += 0.25 * self.others_value

        total_value = min(total_value, 5)

        total_value = total_value / 5

        return total_value

    @property
    def others_value(self):
        value = 0.5

        if self.powerful_recommendation:
            value += 0.2

        if self.olympiad:
            value += 0.2

        if self.related_work_experience:
            if 8 < self.related_work_experience:
                value += 0.2

        if self.academic_break:
            if 4 < self.academic_break:
                value -= 0.2

        value = max(value, 0)
        value = min(value, 1)

        return value

    def _has_age(self):
        return self.age is not None

    def _has_academic_break(self):
        return self.academic_break is not None

    def _has_gender(self):
        return self.gender is not None

    def _has_powerful_recommendation(self):
        return self.powerful_recommendation is not None

    def _has_related_work_experience(self):
        return self.related_work_experience is not None

    def _has_education(self):
        return self.educations.all().exists()

    def get_want_to_apply_or_none(self):
        try:
            return WantToApply.objects.get(student_detailed_info__id=self.id)
        except WantToApply.DoesNotExist:
            return None

    def _has_completed_want_to_apply(self):
        want_to_apply = self.get_want_to_apply_or_none()
        if want_to_apply is None:
            return False
        return want_to_apply.is_complete

    @property
    def is_complete(self):
        completed = True
        for credential in self.completed_credentials:
            completed = completed & getattr(self, credential.get('function_name'))()
        return completed

    def check_is_completed(self, raise_exception=True) -> (bool, list):
        errors = []
        completed = True
        for credential in self.completed_credentials:
            if not getattr(self, credential['function_name'])():
                errors.append(credential['information'])
                completed = False
        if not completed and raise_exception:
            raise DRFValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: {'incomplete_form': errors}
            })
        return completed, errors

    def get_last_university_grade(self):
        return None if self.last_education is None else self.last_education.grade

    #################################
    # Powerful Recommendation methods
    #################################
    def get_powerful_recommendation__store_label(self):
        return MISSING_LABEL if not self.powerful_recommendation or self.powerful_recommendation is None else REWARDED_LABEL

    def get_powerful_recommendation__view_label(self):
        return REWARDED_LABEL if self.powerful_recommendation else MISSING_LABEL

    @classmethod
    def compare_powerful_recommendation_labels(cls, label1, label2):
        if label1 == label2 or label1 == REWARDED_LABEL:
            return label1
        return label2

    def get_powerful_recommendation_user_store_based_positions(self):
        return [self.get_powerful_recommendation__store_label()]

    def get_powerful_recommendation_user_view_based_positions(self):
        return [self.get_powerful_recommendation__view_label()]

    ##################
    # Olympiad methods
    ##################
    def get_olympiad__store_label(self):
        return MISSING_LABEL if self.olympiad is None or len(self.olympiad) == 0 else REWARDED_LABEL

    def get_olympiad__view_label(self):
        return MISSING_LABEL if self.olympiad is None or len(self.olympiad) == 0 else REWARDED_LABEL

    @classmethod
    def compare_olympiad_labels(cls, label1, label2):
        if label1 == label2 or label1 == REWARDED_LABEL:
            return label1
        return label2

    def get_olympiad_user_store_based_positions(self):
        return [self.get_olympiad__store_label()]

    def get_olympiad_user_view_based_positions(self):
        return [self.get_olympiad__view_label()]

    #################################
    # Related Work Experience methods
    #################################
    def get_related_work__store_label(self):
        if self.related_work_experience is None:
            return '0'
        item_range = self.RELATED_WORK_EXPERIENCE_STORE_LABEL_RANGE
        return str(floor(self.related_work_experience / item_range) * item_range)

    def get_related_work__view_label(self):
        if self.related_work_experience >= 36:
            return '36+'
        item_range = self.RELATED_WORK_EXPERIENCE_VIEW_LABEL_RANGE
        value = floor(self.related_work_experience / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def convert_related_work_store_to_view_label(cls, label):
        input_value = int(label)
        if input_value >= 36:
            return '36+'
        item_range = cls.RELATED_WORK_EXPERIENCE_VIEW_LABEL_RANGE
        value = floor(input_value / item_range) * item_range
        return str(value) + ' - ' + str(value + item_range)

    @classmethod
    def compare_related_work_labels(cls, label1, label2):
        if int(label1) >= int(label2):
            return label1
        return label2

    def get_related_work_user_store_based_positions(self):
        return [self.get_related_work__store_label()]

    def get_related_work_user_view_based_positions(self):
        return [self.get_related_work__view_label()]

    @classmethod
    def get_related_work__store_label_rank(cls, label):
        return float(label)

    def save(self, *args, **kwargs):
        self.value = self._compute_value()
        self.rank = self._compute_rank()
        super().save(*args, **kwargs)

