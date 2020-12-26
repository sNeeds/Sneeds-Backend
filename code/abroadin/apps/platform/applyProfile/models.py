from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model

from abroadin.apps.data.account.models import University, Major
from abroadin.apps.data.applyData.models import Education, Publication, LanguageCertificate

User = get_user_model()


class ApplyProfile(models.Model):
    models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    show_name = models.CharField(
        max_length=255,
    )
    latest_degree = models.ForeignKey(
        Education,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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

