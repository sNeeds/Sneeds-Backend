from django.db.models.signals import pre_save, pre_delete, post_save, post_delete, m2m_changed

from abroadin.apps.data.applydata.models import (
    RegularLanguageCertificate,
    GRESubjectCertificate,
    Education,
)
from abroadin.apps.estimation.form.models import (
    Publication,
    LanguageCertificate,
    StudentDetailedInfo,)

from abroadin.apps.estimation.estimations.compute_value import compute_publication_value


def pre_save_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)


def pre_save_university_through(sender, instance, *args, **kwargs):
    instance.value = instance.compute_value()


def post_save_language_certificate(sender, instance, *args, **kwargs):
    # TODO Change coed to be consistence with new form structure
    instance.student_detailed_info.save()


def post_save_student_detailed_info(sender, instance, *args, **kwargs):
    # update_student_detailed_info_ranks()
    pass


def post_save_university_through(sender, instance, *args, **kwargs):
    instance.student_detailed_info.save()


def post_save_publication(sender, instance, *args, **kwargs):
    instance.student_detailed_info.save()


def pre_delete_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)


def post_delete_publication(sender, instance, *args, **kwargs):
    instance.student_detailed_info.save()


def post_delete_university_through(sender, instance, *args, **kwargs):
    instance.student_detailed_info.save()


def post_delete_language_certificate(sender, instance, *args, **kwargs):
    instance.student_detailed_info.save()


post_save.connect(post_save_student_detailed_info, sender=StudentDetailedInfo)
