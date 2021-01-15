from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from abroadin.apps.data.account.models import University, Major, Country
from abroadin.apps.data.applydata.models import Publication, Education, LanguageCertificate

User = get_user_model()


class ApplyProfile(models.Model):
    name = models.CharField(max_length=255)
    academic_gap = models.PositiveSmallIntegerField(help_text='In months', default=0)
    publications = GenericRelation(Publication, related_query_name='apply_profile')
    educations = GenericRelation(Education, related_query_name='apply_profile')
    language_certificates = GenericRelation(LanguageCertificate, related_query_name='apply_profile')


class Admission(models.Model):
    class ScholarshipUnitChoices(models.TextChoices):
        DOLLAR_MONTH = '$/M', _("$/M")
        DOLLAR_YEAR = '$/Y', _("$/Y")
        EURO_MONTH = '€/M', _("€/M")
        EURO_YEAR = '€/Y', _("€/Y")

    apply_profile = models.ForeignKey(ApplyProfile, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, on_delete=models.PROTECT)
    home = models.ForeignKey(
        University, on_delete=models.PROTECT, related_name="admissions_home"
    )
    destination = models.ForeignKey(
        University, on_delete=models.PROTECT, related_name="admissions_destination"
    )
    enroll_year = models.PositiveSmallIntegerField()
    accepted = models.BooleanField()
    scholarship = models.PositiveIntegerField()
    scholarship_unit = models.CharField(
        max_length=8, choices=ScholarshipUnitChoices.choices, help_text='Scholarship unit. For example $/Y or €/M',
    )
    description = models.TextField(max_length=4096, null=True, blank=True, )
