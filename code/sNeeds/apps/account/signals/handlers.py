from django.db.models.signals import pre_save, post_delete, m2m_changed, post_save

from sNeeds.apps.account.models import Publication


def pre_save_publication(sender, instance, *args, **kwargs):
    instance.journal_reputation

pre_save.connect(pre_save_publication, sender=Publication):
