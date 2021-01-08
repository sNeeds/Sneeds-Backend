from django.db.models.signals import pre_save, pre_delete, post_save, post_delete, m2m_changed

from abroadin.apps.estimation.form.models import SDI_CT
from ..models import (
    Publication,
    LanguageCertificate,
    RegularLanguageCertificate,
    GRESubjectCertificate,
    Education
)
from abroadin.apps.estimation.estimations.compute_value import compute_publication_value


def pre_save_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)


def pre_save_education(sender, instance, *args, **kwargs):
    instance.value = instance.compute_value()


def post_save_language_certificate(sender, instance, *args, **kwargs):
    if instance.content_type == SDI_CT:
        instance.content_object.save()
    pass


def post_save_education(sender, instance, *args, **kwargs):
    if instance.content_type == SDI_CT:
        instance.content_object.save()
    pass


def post_save_publication(sender, instance, *args, **kwargs):
    if instance.content_type == SDI_CT:
        instance.content_object.save()
    pass


def pre_delete_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)


def post_delete_publication(sender, instance, *args, **kwargs):
    if instance.content_type == SDI_CT:
        instance.content_object.save()
    pass


def post_delete_education(sender, instance, *args, **kwargs):
    if instance.content_type == SDI_CT:
        instance.content_object.save()
    pass


def post_delete_language_certificate(sender, instance, *args, **kwargs):
    if instance.content_type == SDI_CT:
        instance.content_object.save()


# Signal is not fired when subclasses were updated.
# https://stackoverflow.com/questions/14758250/django-post-save-signal-on-parent-class-with-multi-table-inheritance
for subclass in LanguageCertificate.__subclasses__():
    post_save.connect(post_save_language_certificate, sender=subclass)
    post_delete.connect(post_delete_language_certificate, sender=subclass)

for subclass in RegularLanguageCertificate.__subclasses__():
    post_save.connect(post_save_language_certificate, sender=subclass)
    post_delete.connect(post_delete_language_certificate, sender=subclass)

for subclass in GRESubjectCertificate.__subclasses__():
    post_save.connect(post_save_language_certificate, sender=subclass)
    post_delete.connect(post_delete_language_certificate, sender=subclass)

pre_save.connect(pre_save_publication, sender=Publication)
pre_save.connect(pre_save_education, sender=Education)

post_save.connect(post_save_language_certificate, sender=LanguageCertificate)
post_save.connect(post_save_publication, sender=Publication)
post_save.connect(post_save_education, sender=Education)

pre_delete.connect(pre_delete_publication, sender=Publication)

post_delete.connect(post_delete_publication, sender=Publication)
post_delete.connect(post_delete_education, sender=Education)
