import decimal
import uuid
from math import floor

from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models

from rest_framework.settings import api_settings
from rest_framework.exceptions import ValidationError as DRFValidationError

from abroadin.apps.data.applydata.models import Education, LanguageCertificate, Publication, Grade, SemesterYear,\
    GradeChoices
from abroadin.apps.estimation.estimations.values import VALUES_WITH_ATTRS, LANGUAGE_B_VALUE
from abroadin.apps.estimation.form.variables import MISSING_LABEL, REWARDED_LABEL
from abroadin.apps.estimation.form.managers import StudentDetailedInfoManager

from abroadin.apps.data.account.models import \
    (Country,
     University,
     Major,
     get_student_resume_path,
     User,
     BasicFormField)

from abroadin.apps.data.applydata import models as ad_models

from abroadin.apps.data.account.validators import validate_resume_file_size
from abroadin.base.python.classes import BooleanList

import django.db.models.deletion


class WantToApply(models.Model):
    student_detailed_info = models.OneToOneField(
        'StudentDetailedInfo',
        on_delete=models.CASCADE,
        related_name="want_to_apply",
    )
    # student_detailed_info_old = models.UUIDField(
    # )

    # s = models.ForeignKey()

    countries = models.ManyToManyField(Country, blank=True)

    universities = models.ManyToManyField(University, blank=True)

    grades = models.ManyToManyField(Grade, blank=True)

    majors = models.ManyToManyField(Major, blank=True)

    semester_years = models.ManyToManyField(SemesterYear, blank=True)


class StudentDetailedInfoBase(models.Model):
    # old_id = models.UUIDField()

    # id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='NEW_ID', default=1)

    publications_to_base = GenericRelation(
        Publication, related_query_name='student_detailed_info_base'
    )
    educations_to_base = GenericRelation(
        Education, related_query_name='student_detailed_info_base'
    )
    language_certificates_to_base = GenericRelation(
        LanguageCertificate, related_query_name='student_detailed_info_base'
    )
    regular_certificates_to_base = GenericRelation(
        ad_models.RegularLanguageCertificate, related_query_name='student_detailed_info_base'
    )
    gmat_certificates_to_base = GenericRelation(
        ad_models.GMATCertificate, related_query_name='student_detailed_info_base'
    )
    gre_general_certificates_to_base = GenericRelation(
        ad_models.GREGeneralCertificate, related_query_name='student_detailed_info_base'
    )
    gre_subject_certificates_to_base = GenericRelation(
        ad_models.GRESubjectCertificate, related_query_name='student_detailed_info_base'
    )
    gre_biology_certificates_to_base = GenericRelation(
        ad_models.GREBiologyCertificate, related_query_name='student_detailed_info_base'
    )
    gre_physics_certificates_to_base = GenericRelation(
        ad_models.GREPhysicsCertificate, related_query_name='student_detailed_info_base'
    )
    gre_psychology_certificates_to_base = GenericRelation(
        ad_models.GREPsychologyCertificate, related_query_name='student_detailed_info_base'
    )
    duolingo_certificates_to_base = GenericRelation(
        ad_models.DuolingoCertificate, related_query_name='student_detailed_info_base'
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

    def _university_through_has_this_major(self, major):
        return Education.objects.filter(
            student_detailed_info__id=self.id,
            major=major
        ).exists()

    def university_through_has_these_majors(self, majors_list):
        found = False
        for major in majors_list:
            found = found or self._university_through_has_this_major(major)
        return found

    def last_university_through(self):
        qs = Education.objects.filter(student_detailed_info__id=self.id)
        ordered_qs = qs.order_by_grade()

        if ordered_qs.exists():
            return ordered_qs.last()

        return None

    def language_certificates_str(self):
        return LanguageCertificate.objects.filter(student_detailed_info__id=self.id).brief_str()


class StudentDetailedInfo(models.Model):
    # studentdetailedinfobase_ptr_newid = models.IntegerField(auto_created=True, unique=True, serialize=False, verbose_name='NEW_ID', default=1)
    # studentdetailedinfobase_ptr_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)

    # studentdetailedinfobase_ptr = models.ForeignKey(
    #     StudentDetailedInfoBase, on_delete=models.CASCADE, primary_key=True,
    # )
    # local_new_id = models.ForeignKey(StudentDetailedInfoBase, to_field='new_id', on_delete=models.CASCADE, unique=True),
    # local_new_id = models.ForeignKey(StudentDetailedInfoBase, primary_key=True, serialize=False, default=1)
    # studentdetailedinfobase_ptr = models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='form.studentdetailedinfobase')

    class PaymentAffordabilityChoices(models.TextChoices):
        LOW = 'Low', 'Low'
        AVERAGE = 'Average', 'Average'
        HIGH = 'High', 'High'

    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'

    # If all of these functions return True the form completion definition satisfies
    # The keys are function names
    completed_credentials = [
        {'function_name': "_has_age",
         'information': {'section': 'personal', 'model': 'StudentDetailedInfo', 'fields': ['age'], 'id': 1},
         },
        {'function_name': "_has_is_married",
         'information': {'section': 'personal', 'model': 'StudentDetailedInfo', 'fields': ['is_married'], 'id': 2},
         },
        {'function_name': "_has_gender",
         'information': {'section': 'personal', 'model': 'StudentDetailedInfo', 'fields': ['gender'], 'id': 3},
         },
        # {'function_name': "_has_university_through",
        #  'information': {'section': 'academic_degree', 'model': 'Education', 'fields': [], 'id': 4},
        #  },
        {'function_name': "_has_want_to_apply",
         'information': {'section': 'apply_destination', 'model': 'WantToApply',
                         'fields': ['countries', 'grades', 'semester_years'], 'id': 5},
         },
    ]

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

    gender = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        choices=GenderChoices.choices,
    )

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
    powerful_recommendation = models.BooleanField(
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

    value = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        null=True,
        editable=False
    )

    rank = models.IntegerField(
        validators=[MinValueValidator(1)],
        editable=False
    )

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

    objects = StudentDetailedInfoManager.as_manager()

    class Meta:
        ordering = ['rank', ]

    RELATED_WORK_EXPERIENCE_STORE_LABEL_RANGE = 2
    RELATED_WORK_EXPERIENCE_VIEW_LABEL_RANGE = 6

    def _compute_rank(self):
        better_rank_qs = self.__class__.objects.filter(value__gt=self.value)
        return better_rank_qs.count()

    def _compute_value(self):
        publications = Publication.objects.filter(
            student_detailed_info__id=self.id
        )
        languages = LanguageCertificate.objects.filter(
            student_detailed_info__id=self.id
        )

        total_value = 0

        if self.last_university_through():
            total_value += 2 * self.last_university_through().value

        if languages.exists():
            total_value += languages.get_total_value()
        else:  # when user inputted nothing
            total_value += LANGUAGE_B_VALUE

        total_value += publications.total_value()

        total_value += self.others_value

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
        res = BooleanList()
        # return True
        if self.age is not None:
            return True
        return False

    def _has_is_married(self):
        if self.is_married is not None:
            return True
        return False

    def _has_gender(self):
        if self.gender is not None:
            return True
        return False

    def _has_university_through(self):
        if self.universities.all().exists():
            return True
        return False

    def get_want_to_apply_or_none(self):
        try:
            return WantToApply.objects.get(student_detailed_info__id=self.id)
        except WantToApply.DoesNotExist:
            return None

    def _has_want_to_apply(self):
        check_fields = ['countries', 'grades', 'semester_years']
        want_to_apply = self.get_want_to_apply_or_none()
        if not want_to_apply:
            return False
        completed = True
        non_complete_fields = []
        for field in check_fields:
            if not getattr(want_to_apply, field).exists():
                non_complete_fields.append(field)
                completed = False
        return completed

    def university_through_qs(self):
        return Education.objects.filter(student_detailed_info__id=self.id)

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
        return None if self.last_university_through() is None else self.last_university_through().grade

    def get_related_majors(self):
        related_major_ids = []
        university_through_qs = Education.objects.filter(
            student_detailed_info__id=self.id
        )
        related_major_ids += list(university_through_qs.values_list('major__id', flat=True).distinct())
        try:
            want_to_apply = WantToApply.objects.get(student_detailed_info__id=self.id)
            related_major_ids += list(want_to_apply.majors.all().values_list('id', flat=True).distinct())
        except WantToApply.DoesNotExist:
            pass

        return Major.objects.filter(id__in=related_major_ids)

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
