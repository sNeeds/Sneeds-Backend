from django.core.serializers import serialize
from django.db import transaction
from django.db.models.signals import pre_save, pre_delete, post_save

from sNeeds.apps.estimation.analyze import tasks
from sNeeds.apps.estimation.form.serializers import StudentDetailedInfoCelerySerializer
from sNeeds.apps.estimation.form.tasks import update_student_detailed_info_ranks, \
    add_one_to_rank_with_values_greater_than_this
from sNeeds.apps.estimation.form.models import Publication, LanguageCertificate, StudentDetailedInfo, \
    RegularLanguageCertificate, GRESubjectCertificate, UniversityThrough
from sNeeds.apps.estimation.estimations.compute_value import compute_publication_value


@transaction.atomic
def pre_save_student_detailed_info(sender, instance, *args, **kwargs):
    # TODO: Temporary removed delay from celery tasks
    instance.value = instance.compute_value()
    try:
        previous = StudentDetailedInfo.objects.get(id=instance.id)
        if previous.value != instance.value:  # value is updated
            update_student_detailed_info_ranks(exclude_id=instance.id)
            add_one_to_rank_with_values_greater_than_this(value=instance.value, exclude_id=instance.id)
            instance.rank = instance.update_rank()

    except StudentDetailedInfo.DoesNotExist:  # new object will be created
        update_student_detailed_info_ranks(exclude_id=instance.id)
        add_one_to_rank_with_values_greater_than_this(value=instance.value, exclude_id=instance.id)
        instance.rank = instance.update_rank()

    # https://docs.djangoproject.com/en/3.0/ref/models/instances/#django.db.models.Model._state
    if instance._state.adding is True and instance._state.db is None:
        db_instance = None
    else:
        try:
            db_instance = StudentDetailedInfo.objects.get(pk=instance.pk)
        except StudentDetailedInfo.DoesNotExist:
            db_instance = None

    data = serialize('json', [instance])
    db_data = None if db_instance is None else serialize('json', [db_instance])

    data2 = StudentDetailedInfoCelerySerializer(instance).data
    db_data2 = None if db_instance is None else StudentDetailedInfoCelerySerializer(db_instance).data

    print('self.olympiad', instance.olympiad, type(instance.olympiad))
    print('self.related_work_experience', instance.related_work_experience, type(instance.related_work_experience))

    print(data2)

    # tasks.update_powerful_recommendation_chart.delay(data=data, db_data=db_data, is_delete=False)
    # tasks.update_olympiad_chart.delay(data=data2, db_data=db_data2, is_delete=False)
    # tasks.update_related_work_experience_chart.delay(data=data2, db_data=db_data2, is_delete=False)

    tasks.update_publication_count_chart_sdi_creation.delay(data=data, db_data=db_data, is_delete=False)


def pre_delete_student_detailed_info(sender, instance, *args, **kwargs):
    print("sdi pre delete")
    data = serialize('json', [instance])
    db_data = None

    # tasks.update_powerful_recommendation_chart.delay(data=data, db_data=db_data, is_delete=True)
    # tasks.update_olympiad_chart.delay(data=data, db_data=db_data, is_delete=True)
    # tasks.update_related_work_experience_chart.delay(data=data, db_data=db_data, is_delete=True)

    # publications_count = instance.publication_set.count()
    # # print(publications_count)
    # tasks.update_publication_count_chart_sdi_deletion.delay(publications_count=publications_count,
    #                                                         data=data, db_data=db_data, is_delete=True)


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

    # tasks.update_publication_count_chart.delay(publications_count=publications_count,
    #                                            data=data, db_data=db_data, is_delete=False)
    #
    # tasks.update_publication_type_chart.delay(data=data, db_data=db_data, is_delete=False)
    # tasks.update_publication_impact_factor_chart.delay(data=data, db_data=db_data, is_delete=False)
    # tasks.update_publications_score_chart.delay(data=data, db_data=db_data, is_delete=False)


def pre_delete_publication(sender, instance, *args, **kwargs):
    instance.value = compute_publication_value(instance)
    # tasks.update_publication_count_chart.delay(instance, is_delete=True)
    # tasks.update_publication_type_count_chart.delay(instance, is_delete=True)
    # tasks.update_publication_impact_factor_chart.delay(instance, is_delete=True)
    # tasks.update_publications_score_chart.delay(instance, is_delete=True)


def post_delete_publication(sender, instance, *args, **kwargs):
    print('post delete pub')
    try:
        StudentDetailedInfo.objects.get(id=instance.student_detailed_info.id)
        sdi_exists = True
    except StudentDetailedInfo.DoesNotExist:
        sdi_exists = False

    data = serialize('json', [instance])
    db_data = None

    if sdi_exists:
        publications_count = instance.student_detailed_info.studentdetailedinfo.publication_set.count()
        tasks.update_publication_count_chart.delay(publications_count=publications_count,
                                                   data=data, db_data=db_data, is_delete=True)

    # tasks.update_publication_type_chart.delay(data=data, db_data=db_data, is_delete=True)
    # tasks.update_publication_impact_factor_chart.delay(data=data, db_data=db_data, is_delete=True)
    # tasks.update_publications_score_chart.delay(data=data, db_data=db_data, is_delete=True)


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

    data = serialize('json', [instance])
    db_data = None if db_instance is None else serialize('json', [db_instance])

    # tasks.update_language_certificates_charts.delay(data=data, db_data=db_data, is_delete=False)


def pre_delete_language_certificate(sender, instance, *args, **kwargs):
    data = serialize('json', [instance])
    db_data = None

    # tasks.update_language_certificates_charts.delay(data=data, db_data=db_data, is_delete=True)


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

    # tasks.update_gpa_chart.delay(data=data, db_data=db_data, is_delete=False)


def pre_delete_university_through(sender, instance, *args, **kwargs):
    data = serialize('json', [instance])
    db_data = None
    # tasks.update_gpa_chart.delay(data=data, db_data=db_data, is_delete=True)


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

post_save.connect(post_save_language_certificate, sender=LanguageCertificate)
post_save.connect(post_save_publication, sender=Publication)
post_save.connect(post_save_university_through, sender=UniversityThrough)

pre_delete.connect(pre_delete_publication, sender=Publication)
# pre_delete.connect(pre_delete_language_certificate, sender=LanguageCertificate)
pre_delete.connect(pre_delete_university_through, sender=UniversityThrough)
pre_delete.connect(pre_delete_student_detailed_info, sender=StudentDetailedInfo)
