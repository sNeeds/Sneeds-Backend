from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from abroadin.apps.data.account.models import University, Major, Country
from abroadin.apps.data.applydata.models import Publication, Education, LanguageCertificate, Grade
from abroadin.apps.store.storeBase.models import Product

User = get_user_model()


class ApplyProfile(models.Model):
    name = models.CharField(max_length=255)
    gap = models.PositiveSmallIntegerField(help_text='In months', default=0)
    publications = GenericRelation(Publication, related_query_name='apply_profile')
    educations = GenericRelation(Education, related_query_name='apply_profile')
    language_certificates = GenericRelation(LanguageCertificate, related_query_name='apply_profile')

    def last_education(self):
        education_qs = self.educations.all()
        return education_qs.get_last_grade_education()


class Admission(models.Model):
    apply_profile = models.ForeignKey(
        ApplyProfile, on_delete=models.CASCADE, related_name="admissions", related_query_name="admission"
    )
    major = models.ForeignKey(Major, on_delete=models.PROTECT)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    destination = models.ForeignKey(University, on_delete=models.PROTECT)
    accepted = models.BooleanField()
    scholarship = models.PositiveIntegerField()
    enroll_year = models.PositiveSmallIntegerField()
    description = models.TextField(max_length=4096, null=True, blank=True)

    @classmethod
    def get_unlocked_locked_admissions(cls, admissions: QuerySet) -> tuple:
        """
        @returns a tuple which contains two query sets. first unlocked admissions and second locked admissions
        """
        # admissions = admissions.order_by('enroll_year')
        cls.objects.first()
        unlocked = cls.get_free_admissions(admissions)
        unlocked_ids = unlocked.values_list('id', flat=True)
        locked = admissions.exclude(id__in=unlocked_ids)
        return locked

    @classmethod
    def get_free_admissions(cls, admissions: QuerySet) -> QuerySet:
        admissions = admissions.order_by('enroll_year')
        free = cls.objects.filter(pk=admissions.first().id)
        return free

    @classmethod
    def get_locked_admissions(cls, admissions: QuerySet, free_admissions) -> QuerySet:
        free_ids = free_admissions.values_list('id', flat=True)
        locked = admissions.exclude(id__in=free_ids)
        return locked
