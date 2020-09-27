from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete, m2m_changed, post_save

from sNeeds.apps.account.models import Publication, JournalReputation, WhichAuthor, LanguageCertificate, \
    RegularLanguageCertificate, GRESubjectCertificate, UniversityThrough, StudentDetailedInfo
from sNeeds.apps.estimations.compute_value import compute_publication_value


def pre_save_student_detailed_info(sender, instance, *args, **kwargs):
    instance.value = instance.compute_value()


def pre_save_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)


def post_save_publication(sender, instance, *args, **kwargs):
    instance.student_detailed_info.save()


def pre_save_language_certificate(sender, instance, *args, **kwargs):
    instance.value = instance.compute_value()[0]


def post_save_language_certificate(sender, instance, *args, **kwargs):
    instance.student_detailed_info.save()


def pre_save_university_through(sender, instance, *args, **kwargs):
    instance.value = instance.compute_value()[0]


def post_save_university_through(sender, instance, *args, **kwargs):
    instance.student_detailed_info.save()


# Signal is not fired when subclasses were updated.
# https://stackoverflow.com/questions/14758250/django-post-save-signal-on-parent-class-with-multi-table-inheritance
for subclass in LanguageCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate, sender=subclass)
    post_save.connect(post_save_language_certificate, sender=subclass)

for subclass in RegularLanguageCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate, sender=subclass)
    post_save.connect(post_save_language_certificate, sender=subclass)

for subclass in GRESubjectCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate, sender=subclass)
    post_save.connect(post_save_language_certificate, sender=subclass)

pre_save.connect(pre_save_student_detailed_info, sender=StudentDetailedInfo)
pre_save.connect(pre_save_publication, sender=Publication)
pre_save.connect(pre_save_language_certificate, sender=LanguageCertificate)
pre_save.connect(pre_save_university_through, sender=UniversityThrough)

post_save.connect(post_save_language_certificate, sender=LanguageCertificate)
post_save.connect(post_save_publication, sender=Publication)
post_save.connect(post_save_university_through, sender=UniversityThrough)
