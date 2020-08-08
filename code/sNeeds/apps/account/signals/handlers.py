from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete, m2m_changed, post_save

from sNeeds.apps.account.models import Publication, JournalReputation, WhichAuthor
from sNeeds.apps.estimations.compute_value import compute_publication_value


def pre_save_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)

pre_save.connect(pre_save_publication, sender=Publication)
