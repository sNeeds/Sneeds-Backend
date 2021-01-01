from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


from abroadin.apps.data.account.models import University, Major, Country
from abroadin.apps.data.applydata.models import Publication, Education, LanguageCertificate

User = get_user_model()


def _get_other_country_id():
    """
    Returns a country which is named 'Other'
    """
    qs = Country.objects.filter(name__iexact='Other')
    if qs.exists():
        return qs.first().id
    return Country.objects.create(
        name='Other',
        search_name='other',
        slug='other'
    ).id


def _get_other_university_id():
    """
    Returns a university which is named 'Other'
    """
    qs = University.objects.filter(name__iexact='Other')
    if qs.exists():
        return qs.first().id
    return University.objects.create(
        name='Other',
        search_name='other',
        slug='other',
        country_id=_get_other_country_id(),
        rank=20000,
    ).id


def _get_other_major_id():
    """
        Returns a major which is named 'Other'
    """
    qs = Major.objects.filter(name__iexact='Other')
    if qs.exists():
        return qs.first().id
    return Major.objects.create(
        name='Other',
        search_name='other',
    ).id


class ApplyProfile(models.Model):
    name = models.CharField(
        max_length=255,
    )
    academic_gap = models.PositiveSmallIntegerField(
        help_text='In months',
        default=0,
    )

    publications = GenericRelation(
        Publication, related_query_name='apply_profile'
    )

    educations = GenericRelation(
        Education, related_query_name='apply_profile'
    )

    language_certificates = GenericRelation(
        LanguageCertificate, related_query_name='apply_profile'
    )


class Admission(models.Model):

    class ScholarshipsUnitChoices(models.TextChoices):
        DOLLAR_MONTH = '$/M', _("$/M")
        DOLLAR_YEAR = '$/Y', _("$/Y")
        EURO_MONTH = '€/M', _("€/M")
        EURO_YEAR = '€/Y', _("€/Y")

    apply_profile = models.ForeignKey(
        ApplyProfile,
        on_delete=models.CASCADE,
    )

    enroll_year = models.PositiveSmallIntegerField(
    )

    origin_university = models.ForeignKey(
        University,
        on_delete=models.SET(_get_other_university_id),
        related_name='admission_origin_universities',
        related_query_name='admission_origin_university',
    )

    destination_university = models.ForeignKey(
        University,
        on_delete=models.SET(_get_other_university_id),
        related_name='admission_goal_universities',
        related_query_name='admission_goal_university',
    )

    major = models.ForeignKey(
        Major,
        on_delete=models.SET(_get_other_major_id),
    )

    accepted = models.BooleanField(
        default=False
    )

    scholarships = models.PositiveIntegerField(
    )

    scholarships_unit = models.CharField(
        max_length=8,
        help_text='Scholarship unit. For example $/Y or €/M',
        choices=ScholarshipsUnitChoices.choices,
    )

    description = models.TextField(
        max_length=4096,
        null=True,
        blank=True,
    )
