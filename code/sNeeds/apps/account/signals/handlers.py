from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete

from sNeeds.apps.account.models import Publication, LanguageCertificate, StudentDetailedInfo, \
    RegularLanguageCertificate, GRESubjectCertificate, UniversityThrough

from sNeeds.apps.estimations.compute_value import compute_publication_value

from sNeeds.apps.analyze import tasks


def pre_save_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)
    tasks.update_publication_count_chart.delay(instance, is_delete=False)
    tasks.update_publication_type_count_chart.delay(instance, is_delete=False)
    tasks.update_publication_impact_factor_chart.delay(instance, is_delete=False)
    tasks.update_publications_score_chart.delay(instance, is_delete=False)


def pre_delete_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)
    tasks.update_publication_count_chart.delay(instance, is_delete=True)
    tasks.update_publication_type_count_chart.delay(instance, is_delete=True)
    tasks.update_publication_impact_factor_chart.delay(instance, is_delete=True)
    tasks.update_publications_score_chart.delay(instance, is_delete=True)


def pre_save_language_certificate(sender, instance, *args, **kwargs):
    tasks.update_language_certificates_charts.delay(instance, is_delete=False)


def pre_delete_language_certificate(sender, instance, *args, **kwargs):
    tasks.update_language_certificates_charts.delay(instance, is_delete=True)


def pre_save_university_through(sender, instance, *args, **kwargs):
    tasks.update_gpa_chart.delay(instance, is_delete=False)


def pre_delete_university_through(sender, instance, *args, **kwargs):
    tasks.update_gpa_chart.delay(instance, is_delete=True)


def pre_save_student_detailed_info(sender, instance, *args, **kwargs):
    tasks.update_powerful_recommendation_count_chart.delay(instance, is_delete=False)
    tasks.update_olympiad_count_chart.delay(instance, is_delete=False)
    tasks.update_related_work_experience_chart.delay(instance, is_delete=False)

    tasks.update_publication_count_chart_sdi_creation.delay(instance, is_delete=False)


def pre_delete_student_detailed_info(sender, instance, *args, **kwargs):
    tasks.update_powerful_recommendation_count_chart.delay(instance, is_delete=True)
    tasks.update_olympiad_count_chart.delay(instance, is_delete=True)
    tasks.update_related_work_experience_chart.delay(instance, is_delete=True)

    tasks.update_publication_count_chart_sdi_deletion.delay(instance, is_delete=True)


def pre_save_language_certificate_compute_value(sender, instance, *args, **kwargs):
    instance.value = instance.compute_value()[0]


def pre_save_university_through_compute_value(sender, instance, *args, **kwargs):
    instance.value = instance.compute_value()[0]


# Signal is not fired when subclasses were updated.
# https://stackoverflow.com/questions/14758250/django-post-save-signal-on-parent-class-with-multi-table-inheritance
for subclass in LanguageCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate_compute_value, sender=subclass)

for subclass in RegularLanguageCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate_compute_value, sender=subclass)

for subclass in GRESubjectCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate_compute_value, sender=subclass)

pre_save.connect(pre_save_publication, sender=Publication)
pre_save.connect(pre_save_language_certificate, sender=LanguageCertificate)
pre_save.connect(pre_save_university_through, sender=UniversityThrough)
pre_save.connect(pre_save_student_detailed_info, sender=StudentDetailedInfo)


pre_delete.connect(pre_delete_publication, sender=Publication)
pre_delete.connect(pre_delete_language_certificate, sender=LanguageCertificate)
pre_delete.connect(pre_delete_university_through, sender=UniversityThrough)
pre_delete.connect(pre_delete_student_detailed_info, sender=StudentDetailedInfo)
pre_save.connect(pre_save_language_certificate, sender=LanguageCertificate)
pre_save.connect(pre_save_university_through, sender=UniversityThrough)
