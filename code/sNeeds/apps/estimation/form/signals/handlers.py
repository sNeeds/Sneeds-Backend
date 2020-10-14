from django.core.serializers import serialize
from django.db import transaction
from django.db.models.signals import pre_save, pre_delete, post_save

from sNeeds.apps.estimation.analyze import update_charts
from sNeeds.apps.estimation.form.serializers import StudentDetailedInfoCelerySerializer
from sNeeds.apps.estimation.form.tasks import update_student_detailed_info_ranks, \
    add_one_to_rank_with_values_greater_than_this
from sNeeds.apps.estimation.form.models import Publication, LanguageCertificate, StudentDetailedInfo, \
    RegularLanguageCertificate, GRESubjectCertificate, UniversityThrough
from sNeeds.apps.estimation.estimations.compute_value import compute_publication_value
from sNeeds.apps.estimation.form import serializers as form_serializers


@transaction.atomic
def pre_save_student_detailed_info(sender, instance, *args, **kwargs):
    # TODO: Temporary removed delay from celery tasks
    try:
        StudentDetailedInfo.objects.get(id=instance.id)

    except StudentDetailedInfo.DoesNotExist:  # new object will be created
        pass


    # https://docs.djangoproject.com/en/3.0/ref/models/instances/#django.db.models.Model._state
    if instance._state.adding is True and instance._state.db is None:
        db_instance = None
    else:
        try:
            db_instance = StudentDetailedInfo.objects.get(pk=instance.pk)
        except StudentDetailedInfo.DoesNotExist:
            db_instance = None

    data = form_serializers.StudentDetailedInfoCelerySerializer(instance).data
    db_data = None if db_instance is None else form_serializers.StudentDetailedInfoCelerySerializer(
        db_instance).data

    update_charts.update_powerful_recommendation_chart.delay(data=data, db_data=db_data, is_delete=False)
    update_charts.update_olympiad_chart.delay(data=data, db_data=db_data, is_delete=False)
    update_charts.update_related_work_experience_chart.delay(data=data, db_data=db_data, is_delete=False)

    update_charts.update_publication_count_chart_sdi_creation.delay(data=data, db_data=db_data, is_delete=False)


def pre_delete_student_detailed_info(sender, instance, *args, **kwargs):
    data = form_serializers.StudentDetailedInfoCelerySerializer(instance).data
    db_data = None

    update_charts.update_powerful_recommendation_chart.delay(data=data, db_data=db_data, is_delete=True)
    update_charts.update_olympiad_chart.delay(data=data, db_data=db_data, is_delete=True)
    update_charts.update_related_work_experience_chart.delay(data=data, db_data=db_data, is_delete=True)

    publications_count = instance.publication_set.count()

    update_charts.update_publication_count_chart_sdi_deletion.delay(publications_count=publications_count,
                                                                    data=data, db_data=db_data, is_delete=True)


def pre_save_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)

    if instance._state.adding is True and instance._state.db is None:
        db_instance = None
    else:
        try:
            db_instance = Publication.objects.get(pk=instance.pk)
        except Publication.DoesNotExist:
            db_instance = None

    data = serialize('json', [instance])
    db_data = None if db_instance is None else serialize('json', [db_instance])

    publications_count = instance.student_detailed_info.studentdetailedinfo.publication_set.count()

    update_charts.update_publication_count_chart.delay(publications_count=publications_count,
                                                       data=data, db_data=db_data, is_delete=False)

    update_charts.update_publication_type_chart.delay(data=data, db_data=db_data, is_delete=False)
    update_charts.update_publication_impact_factor_chart.delay(data=data, db_data=db_data, is_delete=False)
    # update_charts.update_publications_score_chart.delay(data=data, db_data=db_data, is_delete=False)


def pre_delete_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)


def post_delete_publication(sender, instance, *args, **kwargs):
    try:
        StudentDetailedInfo.objects.get(id=instance.student_detailed_info.id)
        sdi_exists = True
    except StudentDetailedInfo.DoesNotExist:
        sdi_exists = False

    data = serialize('json', [instance])
    db_data = None

    if sdi_exists:
        publications_count = instance.student_detailed_info.studentdetailedinfo.publication_set.count()
        update_charts.update_publication_count_chart.delay(publications_count=publications_count,
                                                           data=data, db_data=db_data, is_delete=True)

    update_charts.update_publication_type_chart.delay(data=data, db_data=db_data, is_delete=True)
    update_charts.update_publication_impact_factor_chart.delay(data=data, db_data=db_data, is_delete=True)
    # update_charts.update_publications_score_chart.delay(data=data, db_data=db_data, is_delete=True)


def post_save_student_detailed_info(sender, instance, *args, **kwargs):
    update_student_detailed_info_ranks()


def post_save_publication(sender, instance, *args, **kwargs):
    instance.student_detailed_info.save()


def pre_save_language_certificate(sender, instance, *args, **kwargs):
    instance.value = instance.compute_value()[0]

    if instance._state.adding is True and instance._state.db is None:
        db_instance = None
    else:
        try:
            db_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            db_instance = None

    data = update_charts.serialize_language_certificate(instance)
    db_data = None if db_instance is None else update_charts.serialize_language_certificate(db_instance)

    update_charts.update_language_certificates_charts.delay(data=data, db_data=db_data, is_delete=False)


def pre_delete_language_certificate(sender, instance, *args, **kwargs):
    data = update_charts.serialize_language_certificate(instance)
    db_data = None

    # skip if sender is parent class
    if sender == GRESubjectCertificate and instance.certificate_type in \
            [LanguageCertificate.LanguageCertificateType.GRE_PHYSICS,
             LanguageCertificate.LanguageCertificateType.GRE_BIOLOGY,
             LanguageCertificate.LanguageCertificateType.GRE_PSYCHOLOGY]:
        pass
    else:
        update_charts.update_language_certificates_charts.delay(data=data, db_data=db_data, is_delete=True)


def post_save_language_certificate(sender, instance, *args, **kwargs):
    instance.student_detailed_info.save()


def pre_save_university_through(sender, instance, *args, **kwargs):
    instance.value = instance.compute_value()

    if instance._state.adding is True and instance._state.db is None:
        db_instance = None
    else:
        try:
            db_instance = UniversityThrough.objects.get(pk=instance.pk)
        except UniversityThrough.DoesNotExist:
            db_instance = None

    data = serialize('json', [instance])
    db_data = None if db_instance is None else serialize('json', [db_instance])

    new_label, old_label = update_charts.pre_update_update_gpa_chart(instance, db_instance, is_delete=False)
    update_charts.update_gpa_chart.delay(new_label=new_label, old_label=old_label)


def pre_delete_university_through(sender, instance, *args, **kwargs):
    data = serialize('json', [instance])
    db_data = None
    db_instance = None
    new_label, old_label = update_charts.pre_update_update_gpa_chart(instance, db_instance, is_delete=True)
    update_charts.update_gpa_chart.delay(new_label=new_label, old_label=old_label)


def post_save_university_through(sender, instance, *args, **kwargs):
    instance.student_detailed_info.save()


# Signal is not fired when subclasses were updated.
# https://stackoverflow.com/questions/14758250/django-post-save-signal-on-parent-class-with-multi-table-inheritance
for subclass in LanguageCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate, sender=subclass)
    post_save.connect(post_save_language_certificate, sender=subclass)
    pre_delete.connect(pre_delete_language_certificate, sender=subclass)

for subclass in RegularLanguageCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate, sender=subclass)
    post_save.connect(post_save_language_certificate, sender=subclass)
    pre_delete.connect(pre_delete_language_certificate, sender=subclass)

for subclass in GRESubjectCertificate.__subclasses__():
    pre_save.connect(pre_save_language_certificate, sender=subclass)
    post_save.connect(post_save_language_certificate, sender=subclass)
    pre_delete.connect(pre_delete_language_certificate, sender=subclass)

pre_save.connect(pre_save_student_detailed_info, sender=StudentDetailedInfo)
pre_save.connect(pre_save_publication, sender=Publication)
pre_save.connect(pre_save_language_certificate, sender=LanguageCertificate)
pre_save.connect(pre_save_university_through, sender=UniversityThrough)

post_save.connect(post_save_student_detailed_info, sender=StudentDetailedInfo)
post_save.connect(post_save_language_certificate, sender=LanguageCertificate)
post_save.connect(post_save_publication, sender=Publication)
post_save.connect(post_save_university_through, sender=UniversityThrough)

pre_delete.connect(pre_delete_publication, sender=Publication)
# pre_delete.connect(pre_delete_language_certificate, sender=LanguageCertificate)
pre_delete.connect(pre_delete_university_through, sender=UniversityThrough)
pre_delete.connect(pre_delete_student_detailed_info, sender=StudentDetailedInfo)
