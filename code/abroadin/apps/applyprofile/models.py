from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from abroadin.apps.applyprofile.managers import AdmissionQuerySet
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
        return education_qs.last_education()

    def main_admission(self):
        admission_qs = self.admissions.all()
        qs = admission_qs.order_by('-destination__rank').order_by_grade()
        if qs.exists():
            return qs.last()
        return None

    def get_free_locked_admissions(self) -> tuple:
        """
        @returns a tuple which contains two query sets. first unlocked admissions and second locked admissions
        """
        free = self.get_free_admissions()
        locked = self.get_locked_admissions(free)
        return free, locked

    def get_free_admissions(self) -> QuerySet:
        # admissions = self.admissions.order_by('enroll_year')
        # free = self.admissions.filter(pk=admissions.first().id)
        return self.admissions.all()

    def get_locked_admissions(self, free_admissions) -> QuerySet:
        free_ids = free_admissions.values_list('id', flat=True)
        locked = self.admissions.exclude(id__in=free_ids)
        return locked

    def get_free_locked_publications(self) -> tuple:
        """
        @returns a tuple which contains two query sets. first unlocked publication and second locked publications
        """
        free = self.get_free_publications()
        locked = self.get_locked_publications(free)
        return free, locked

    def get_free_publications(self) -> QuerySet:
        publications = self.publications.order_by('enroll_year')
        free = publications.filter(pk=publications.first().id)
        return free

    def get_locked_publications(self, free_publications: QuerySet) -> QuerySet:
        free_ids = free_publications.values_list('id', flat=True)
        locked = self.publications.exclude(id__in=free_ids)
        return locked

    def get_free_locked_educations(self) -> tuple:
        """
        @returns a tuple which contains two query sets. first unlocked education and second locked educations
        """
        free = self.get_free_educations()
        locked = self.get_locked_educations(free)
        return free, locked

    def get_free_educations(self) -> QuerySet:
        free = self.educations.all()
        return free

    def get_locked_educations(self, free_educations: QuerySet) -> QuerySet:
        free_ids = free_educations.values_list('id', flat=True)
        locked = self.educations.exclude(id__in=free_ids)
        return locked

    def get_free_locked_language_certificates(self) -> tuple:
        """
        @returns a tuple which contains two query sets. first unlocked language_certificate and second locked language_certificates
        """
        free = self.get_free_language_certificates()
        locked = self.get_locked_language_certificates(free)
        return free, locked

    def get_free_language_certificates(self) -> QuerySet:
        free = self.language_certificates.none()
        return free

    def get_locked_language_certificates(self, free_language_certificates: QuerySet) -> QuerySet:
        locked = self.language_certificates.none()
        return locked


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

    objects = AdmissionQuerySet.as_manager()

