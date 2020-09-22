from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete, m2m_changed, post_save

from sNeeds.apps.account.models import Publication, JournalReputation, WhichAuthor, LanguageCertificate, \
    RegularLanguageCertificate, GRESubjectCertificate
from sNeeds.apps.estimations.compute_value import compute_publication_value, compute_language_certificate_value


def pre_save_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)


def pre_save_language_certificate(sender, instance, *args, **kwargs):
    instance.value = compute_language_certificate_value(instance)[0]


# Signal is not fired when subclasses were updated.
# https://stackoverflow.com/questions/14758250/django-post-save-signal-on-parent-class-with-multi-table-inheritance
for subclass in LanguageCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate, sender=subclass)

for subclass in RegularLanguageCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate, sender=subclass)

for subclass in GRESubjectCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate, sender=subclass)

pre_save.connect(pre_save_publication, sender=Publication)
pre_save.connect(pre_save_language_certificate, sender=LanguageCertificate)
