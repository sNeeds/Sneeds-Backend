from celery import shared_task

from django.core.serializers import deserialize, serialize
from django.db.models import Sum, F
from django.db import transaction

from abroadin.apps.estimation.form import models as form_models
from abroadin.apps.data.applydata import models as ad_models
from abroadin.apps.estimation.form import managers as form_managers
from abroadin.apps.estimation.analyze.models import Chart, ChartItemData
from abroadin.apps.estimation.form.serializers import StudentDetailedInfoCelerySerializer
from abroadin.apps.estimation.form import serializers as form_serializers
from abroadin.apps.estimation.form.models import StudentDetailedInfo

LanguageCertificateType = form_models.LanguageCertificate.LanguageCertificateType


@shared_task
def update_powerful_recommendation_chart(data, db_data, is_delete=False):
    serializer = StudentDetailedInfoCelerySerializer(data=data)
    serializer.is_valid()
    instance = form_models.StudentDetailedInfo(**serializer.validated_data)

    if db_data is None:
        db_instance = None
    else:
        serializer = StudentDetailedInfoCelerySerializer(data=db_data)
        serializer.is_valid()
        db_instance = form_models.StudentDetailedInfo(**serializer.validated_data)

    update_common_chart(Chart.ChartTitle.POWERFUL_RECOMMENDATION, form_models.StudentDetailedInfo,
                        form_models.StudentDetailedInfo.get_powerful_recommendation__store_label,
                        instance, db_instance, is_delete)


@shared_task
def update_olympiad_chart(data, db_data, is_delete=False):
    serializer = StudentDetailedInfoCelerySerializer(data=data)
    serializer.is_valid()
    instance = form_models.StudentDetailedInfo(**serializer.validated_data)

    if db_data is None:
        db_instance = None
    else:
        serializer = StudentDetailedInfoCelerySerializer(data=db_data)
        serializer.is_valid()
        db_instance = form_models.StudentDetailedInfo(**serializer.validated_data)

    update_common_chart(Chart.ChartTitle.OLYMPIAD, form_models.StudentDetailedInfo,
                        form_models.StudentDetailedInfo.get_olympiad__store_label, instance, db_instance, is_delete)


@shared_task
def update_related_work_experience_chart(data, db_data, is_delete=False):
    serializer = StudentDetailedInfoCelerySerializer(data=data)
    serializer.is_valid()
    instance = form_models.StudentDetailedInfo(**serializer.validated_data)

    if db_data is None:
        db_instance = None
    else:
        serializer = StudentDetailedInfoCelerySerializer(data=db_data)
        serializer.is_valid()
        db_instance = form_models.StudentDetailedInfo(**serializer.validated_data)

    update_common_chart(Chart.ChartTitle.RELATED_WORK_EXPERIENCE, form_models.StudentDetailedInfo,
                        form_models.StudentDetailedInfo.get_related_work__store_label, instance, db_instance,
                        is_delete)


def update_publication_count_chart(instance, db_instance, is_delete=False):
    """
        this function should be called in post delete state
    """
    try:
        sdi = instance.student_detailed_info.studentdetailedinfo
        publications_count = form_models.Publication.objects.filter(student_detailed_info__id=sdi.id).count()
        data = serialize('json', [instance])
        db_data = None if db_instance is None else serialize('json', [db_instance])

        update_publication_count_chart_by_count.delay(
            publications_count=publications_count, data=data, db_data=db_data, is_delete=is_delete
        )

    except StudentDetailedInfo.DoesNotExist:
        pass


@shared_task
def update_publication_count_chart_by_count(publications_count, data, db_data, is_delete=False):
    """
    this function for delete signal should be called in post_delete
    :return:
    """

    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.PUBLICATIONS_COUNT)

    if is_delete:
        old_label = str(publications_count + 1)

        with transaction.atomic():
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                               defaults={'count': 0})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)

        if publications_count < 0:
            raise Exception("Error in publication count label calculation. Below zero label produced.")

        new_label = str(publications_count)
        with transaction.atomic():
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                               defaults={'count': 1})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)

    else:
        # Save has been called in order to update an entry
        if db_instance is not None:
            pass
        # Save has been called in order to create an entry
        else:
            old_label = str(publications_count)

            with transaction.atomic():
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                                   defaults={'count': 0})
                if not created:
                    ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)

            new_label = str(publications_count + 1)

            with transaction.atomic():
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                                   defaults={'count': 1})
                if not created:
                    ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)


def update_publications_score_chart(instance, db_instance, is_delete=False):
    """
    this function should be called in post delete state
    """
    try:
        instance.student_detailed_info.studentdetailedinfo
    except StudentDetailedInfo.DoesNotExist:
        return
    new_label, old_label = prepare_publications_score_chart_data(instance, db_instance, is_delete)
    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.PUBLICATIONS_SCORE)
    chart_data = serialize('json', [chart])
    update_chart_by_label.delay(chart_data, new_label=new_label, old_label=old_label)


def prepare_publications_score_chart_data(instance, db_instance, is_delete=False):
    """
        this function should be called in post delete state
    """
    if is_delete:
        remained_publications = instance.student_detailed_info.studentdetailedinfo.publication_set.all() \
            .order_by('-value')
        new_publications_score = remained_publications.total_value()

        old_publications_list = list(remained_publications)
        old_publications_list.append(instance)
        old_publications_list.sort(key=lambda x: x.value, reverse=True)

        old_publications_score = form_managers.PublicationQuerySetManager.calculate_value(old_publications_list)

        old_label = form_models.Publication.get_publications_score__store_label(old_publications_score)
        new_label = form_models.Publication.get_publications_score__store_label(new_publications_score)

    else:
        # Save has been called in order to update an entry
        if db_instance is not None:
            old_publications_score = instance.student_detailed_info.studentdetailedinfo.publication_set.total_value()

            except_instance_publications = instance.student_detailed_info.studentdetailedinfo.publication_set.exclude(
                pk=instance.pk).order_by('-value')

            new_publications_list = list(except_instance_publications)
            new_publications_list.append(instance)
            new_publications_list.sort(key=lambda x: x.value, reverse=True)

            new_publications_score = form_managers.PublicationQuerySetManager.calculate_value(new_publications_list)

            old_label = form_models.Publication.get_publications_score__store_label(old_publications_score)
            new_label = form_models.Publication.get_publications_score__store_label(new_publications_score)

        # Save has been called in order to create an entry
        else:
            old_publications = instance.student_detailed_info.studentdetailedinfo.publication_set.all().order_by(
                '-value')
            old_publications_score = old_publications.total_value()

            new_publications_list = list(old_publications)
            new_publications_list.append(instance)
            new_publications_list.sort(key=lambda x: x.value, reverse=True)

            new_publications_score = form_managers.PublicationQuerySetManager.calculate_value(new_publications_list)

            old_label = form_models.Publication.get_publications_score__store_label(old_publications_score)
            new_label = form_models.Publication.get_publications_score__store_label(new_publications_score)

    return new_label, old_label


def update_charts_sdi_creation(data, db_data, is_delete=False):
    update_publications_count_chart_sdi_creation.delay(data, db_data, is_delete)
    update_publications_score_chart_sdi_creation.delay(data, db_data, is_delete)


@shared_task()
def update_publications_count_chart_sdi_creation(data, db_data, is_delete=False):
    if db_data is None:
        db_instance = None
    else:
        serializer = StudentDetailedInfoCelerySerializer(data=db_data)
        serializer.is_valid()
        db_instance = form_models.StudentDetailedInfo(**serializer.validated_data)

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.PUBLICATIONS_COUNT)

    # Save has been called in order to update an entry
    if db_instance is not None:
        pass
    # Save has been called in order to create an entry
    else:
        label = '0'

        with transaction.atomic():
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                               defaults={'count': 1})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)


@shared_task()
def update_publications_score_chart_sdi_creation(data, db_data, is_delete=False):
    if db_data is None:
        db_instance = None
    else:
        serializer = StudentDetailedInfoCelerySerializer(data=db_data)
        serializer.is_valid()
        db_instance = form_models.StudentDetailedInfo(**serializer.validated_data)

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.PUBLICATIONS_SCORE)

    # Save has been called in order to update an entry
    if db_instance is not None:
        pass
    # Save has been called in order to create an entry
    else:
        label = '0.0'

        with transaction.atomic():
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                               defaults={'count': 1})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)


def update_charts_sdi_deletion(instance, db_instance, is_delete=False):
    # serializer = StudentDetailedInfoCelerySerializer(data=data)
    # serializer.is_valid()
    # instance = form_models.StudentDetailedInfo(**serializer.validated_data)
    #
    # if db_data is None:
    #     db_instance = None
    # else:
    #     serializer = StudentDetailedInfoCelerySerializer(data=db_data)
    #     serializer.is_valid()
    #     db_instance = form_models.StudentDetailedInfo(**serializer.validated_data)

    data = form_serializers.StudentDetailedInfoCelerySerializer(instance).data
    db_data = None

    publications_count = instance.publication_set.count()
    update_publications_count_chart_sdi_deletion.delay(publications_count, data, db_data, is_delete)

    publications_score = instance.publication_set.total_value()
    update_publications_score_chart_sdi_deletion.delay(publications_score, data, db_data, is_delete)


@shared_task()
def update_publications_count_chart_sdi_deletion(publications_count, data, db_data, is_delete=False):
    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.PUBLICATIONS_COUNT)

    if is_delete:

        label = str(publications_count)

        with transaction.atomic():
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                               defaults={'count': 0})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)


@shared_task()
def update_publications_score_chart_sdi_deletion(publications_score, data, db_data, is_delete=False):
    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.PUBLICATIONS_SCORE)

    if is_delete:

        label = form_models.Publication.get_publications_score__store_label(publications_score)

        with transaction.atomic():
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                               defaults={'count': 0})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)


@shared_task
def update_publication_type_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object

    update_common_chart(Chart.ChartTitle.PUBLICATION_TYPE, form_models.Publication,
                        form_models.Publication.get_type__store_label, instance, db_instance, is_delete)


@shared_task
def update_publication_impact_factor_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    update_common_chart(Chart.ChartTitle.PUBLICATION_IMPACT_FACTOR, form_models.Publication,
                        form_models.Publication.get_impact_factor__store_label, instance, db_instance, is_delete)


def update_gpa_chart(instance, db_instance, is_delete=False):
    new_label, old_label = prepare_update_gpa_chart(instance, db_instance, is_delete)
    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.GRADE_POINT_AVERAGE)
    chart_data = serialize('json', [chart])
    update_chart_by_label.delay(chart_data, new_label=new_label, old_label=old_label)


def prepare_update_gpa_chart(instance, db_instance, is_delete=False):
    old_label = None
    new_label = None
    if is_delete:
        qs = ad_models.Education.objects.filter(student_detailed_info__id=instance.student_detailed_info.id). \
            order_by('-graduate_in')
        last_grade = qs.first()
        # We check that the instance is the last education is being removed from sdi educations set
        if last_grade == instance:
            old_label = form_models.Education.get_gpa__store_label(last_grade)
            # now we look for last grade after instance
            new_last_grade = qs.exclude(pk=instance.pk).first()
            if new_last_grade is not None:
                new_label = form_models.Education.get_gpa__store_label(new_last_grade)
            else:
                new_label = None
        else:
            old_label = None
    else:
        if db_instance is not None:
            qs = form_models.Education.objects.filter(
                student_detailed_info__id=instance.student_detailed_info.id
            ).order_by('-graduate_in')

            are_labels_updated = False

            last_grade = qs.first()
            next_last_grade = qs.exclude(pk=instance.pk).first()

            if instance.pk == last_grade.pk:
                # we check that the instance graduate has changed and is not going to be the last grade any more
                if instance.graduate_in < last_grade.graduate_in \
                        and next_last_grade is not None and instance.graduate_in < next_last_grade.graduate_in:
                    old_label = form_models.Education.get_gpa__store_label(last_grade)
                    new_label = form_models.Education.get_gpa__store_label(next_last_grade)
                    are_labels_updated = True

                # We check gpa changes. If we do not enter the previous if statement it means the instance still is
                # last grade.We check that by is_chart_updated flag.
                if instance.gpa != db_instance.gpa and not are_labels_updated:
                    old_label = form_models.Education.get_gpa__store_label(db_instance)
                    new_label = form_models.Education.get_gpa__store_label(instance)

            # The instance was not last grade education but maybe it become last grade by increasing graduate_in value!
            elif instance.graduate_in > last_grade.graduate_in:
                old_label = form_models.Education.get_gpa__store_label(last_grade)
                new_label = form_models.Education.get_gpa__store_label(instance)

        # Save has been called in order to create an entry
        else:
            qs = form_models.Education.objects.filter(
                student_detailed_info__id=instance.student_detailed_info.id
            ).order_by('-graduate_in')

            last_grade = qs.first()

            if last_grade is None:
                new_label = form_models.Education.get_gpa__store_label(instance)

            elif instance.graduate_in > last_grade.graduate_in:
                old_label = form_models.Education.get_gpa__store_label(last_grade)
                new_label = form_models.Education.get_gpa__store_label(instance)

    return new_label, old_label


def serialize_language_certificate(instance) -> dict:
    if instance.certificate_type == LanguageCertificateType.IELTS_GENERAL or \
            instance.certificate_type == LanguageCertificateType.IELTS_ACADEMIC or \
            instance.certificate_type == LanguageCertificateType.TOEFL:
        return form_serializers.RegularLanguageCertificateCelerySerializer(instance).data

    elif instance.certificate_type == LanguageCertificateType.GMAT:
        return form_serializers.GMATCertificateCelerySerializer(instance).data

    elif instance.certificate_type == LanguageCertificateType.GRE_GENERAL:
        return form_serializers.GREGeneralCertificateCelerySerializer(instance).data

    elif instance.certificate_type == LanguageCertificateType.GRE_MATHEMATICS or \
            instance.certificate_type == LanguageCertificateType.GRE_CHEMISTRY or \
            instance.certificate_type == LanguageCertificateType.GRE_LITERATURE:
        return form_serializers.GRESubjectCertificateCelerySerializer(instance).data

    elif instance.certificate_type == LanguageCertificateType.GRE_PHYSICS or \
            instance.certificate_type == LanguageCertificateType.GRE_BIOLOGY or \
            instance.certificate_type == LanguageCertificateType.GRE_PSYCHOLOGY:
        return form_serializers.GRESubjectCertificateCelerySerializer(instance).data

    elif instance.certificate_type == LanguageCertificateType.DUOLINGO:
        return form_serializers.DuolingoCertificateCelerySerializer(instance).data

    raise Exception("Program should not reach here.")


def deserialize_language_certificate(data: dict):
    certificate_type = data.get('certificate_type')

    serializer_class = None
    model_class = None

    if certificate_type == LanguageCertificateType.IELTS_GENERAL or \
            certificate_type == LanguageCertificateType.IELTS_ACADEMIC or \
            certificate_type == LanguageCertificateType.TOEFL:
        serializer_class = form_serializers.RegularLanguageCertificateCelerySerializer
        model_class = form_models.RegularLanguageCertificate

    elif certificate_type == LanguageCertificateType.GMAT:
        serializer_class = form_serializers.GMATCertificateCelerySerializer
        model_class = form_models.GMATCertificate

    elif certificate_type == LanguageCertificateType.GRE_GENERAL:
        serializer_class = form_serializers.GREGeneralCertificateCelerySerializer
        model_class = form_models.GREGeneralCertificate

    elif certificate_type == LanguageCertificateType.GRE_MATHEMATICS or \
            certificate_type == LanguageCertificateType.GRE_CHEMISTRY or \
            certificate_type == LanguageCertificateType.GRE_LITERATURE:
        serializer_class = form_serializers.GRESubjectCertificateCelerySerializer
        model_class = form_models.GRESubjectCertificate

    elif certificate_type == LanguageCertificateType.GRE_PHYSICS or \
            certificate_type == LanguageCertificateType.GRE_BIOLOGY or \
            certificate_type == LanguageCertificateType.GRE_PSYCHOLOGY:
        serializer_class = form_serializers.GRESubjectCertificateCelerySerializer
        model_class = form_models.GRESubjectCertificate

    elif certificate_type == LanguageCertificateType.DUOLINGO:
        serializer_class = form_serializers.DuolingoCertificateCelerySerializer
        model_class = form_models.DuolingoCertificate

    serializer = serializer_class(data=data)
    if not serializer.is_valid():
        raise Exception('invalid data or faulty serializer')
    instance = model_class(**serializer.validated_data)
    return instance


@shared_task
def update_language_certificates_charts(data: dict, db_data, is_delete=False):
    certificate_type = data.get('certificate_type')

    if certificate_type == LanguageCertificateType.IELTS_GENERAL or \
            certificate_type == LanguageCertificateType.IELTS_ACADEMIC:
        update_ielts_chart(data=data, db_data=db_data, is_delete=is_delete)

    elif certificate_type == LanguageCertificateType.TOEFL:
        update_toefl_chart(data=data, db_data=db_data, is_delete=is_delete)

    elif certificate_type == LanguageCertificateType.GMAT:
        update_gmat_chart(data=data, db_data=db_data, is_delete=is_delete)

    elif certificate_type == LanguageCertificateType.GRE_GENERAL:
        update_gre_general_writing_chart(data=data, db_data=db_data, is_delete=is_delete)
        update_gre_general_quantitative_and_verbal_chart(data=data, db_data=db_data, is_delete=is_delete)

    elif certificate_type == LanguageCertificateType.GRE_MATHEMATICS or \
            certificate_type == LanguageCertificateType.GRE_CHEMISTRY or \
            certificate_type == LanguageCertificateType.GRE_LITERATURE or \
            certificate_type == LanguageCertificateType.GRE_PHYSICS or \
            certificate_type == LanguageCertificateType.GRE_BIOLOGY or \
            certificate_type == LanguageCertificateType.GRE_PSYCHOLOGY:
        update_gre_subject_total_chart(data=data, db_data=db_data, is_delete=is_delete)

    elif certificate_type == LanguageCertificateType.DUOLINGO:
        update_duolingo_chart(data=data, db_data=db_data, is_delete=is_delete)

    # elif certificate_type == account_models.LanguageCertificateType.GRE_PHYSICS:
    #     update_gre_physics_chart(instance=instance, is_delete=is_delete)
    #
    # elif certificate_type == account_models.LanguageCertificateType.GRE_BIOLOGY:
    #     update_gre_biology_chart(instance=instance, is_delete=is_delete)
    #
    # elif certificate_type == account_models.LanguageCertificateType.GRE_PSYCHOLOGY:
    #     update_gre_psychology_chart(instance=instance, is_delete=is_delete)


def update_ielts_chart(data, db_data, is_delete=False):
    instance = deserialize_language_certificate(data=data)

    if db_data is None:
        db_instance = None
    else:
        db_instance = deserialize_language_certificate(data=db_data)

    update_common_chart(Chart.ChartTitle.IELTS, form_models.RegularLanguageCertificate,
                        form_models.RegularLanguageCertificate.get_ielts__store_label,
                        instance, db_instance, is_delete)


def update_toefl_chart(data, db_data, is_delete=False):
    instance = deserialize_language_certificate(data=data)
    if db_data is None:
        db_instance = None
    else:
        db_instance = deserialize_language_certificate(data=db_data)

    update_common_chart(Chart.ChartTitle.TOEFL, form_models.RegularLanguageCertificate,
                        form_models.RegularLanguageCertificate.get_toefl__store_label,
                        instance, db_instance, is_delete)


def update_gmat_chart(data, db_data, is_delete=False):
    instance = deserialize_language_certificate(data=data)

    if db_data is None:
        db_instance = None
    else:
        db_instance = deserialize_language_certificate(data=db_data)

    update_common_chart(Chart.ChartTitle.GMAT, form_models.GMATCertificate,
                        form_models.GMATCertificate.get_store_label,
                        instance, db_instance, is_delete)


def update_gre_general_writing_chart(data, db_data, is_delete=False):
    instance = deserialize_language_certificate(data=data)

    if db_data is None:
        db_instance = None
    else:
        db_instance = deserialize_language_certificate(data=db_data)
    update_common_chart(Chart.ChartTitle.GRE_GENERAL_WRITING, form_models.GREGeneralCertificate,
                        form_models.GREGeneralCertificate.get_writing_store_label, instance, db_instance, is_delete)


def update_gre_general_quantitative_and_verbal_chart(data, db_data, is_delete=False):
    instance = deserialize_language_certificate(data=data)

    if db_data is None:
        db_instance = None
    else:
        db_instance = deserialize_language_certificate(data=db_data)
    update_common_chart(Chart.ChartTitle.GRE_GENERAL_QUANTITATIVE_AND_VERBAL, form_models.GREGeneralCertificate,
                        form_models.GREGeneralCertificate.get_q_and_v_store_label, instance, db_instance, is_delete)


def update_gre_subject_total_chart(data, db_data, is_delete=False):
    instance = deserialize_language_certificate(data=data)

    if db_data is None:
        db_instance = None
    else:
        db_instance = deserialize_language_certificate(data=db_data)
    update_common_chart(Chart.ChartTitle.GRE_SUBJECT_TOTAL, form_models.GRESubjectCertificate,
                        form_models.GRESubjectCertificate.get_total_store_label, instance, db_instance, is_delete)


def update_duolingo_chart(data, db_data, is_delete=False):
    instance = deserialize_language_certificate(data=data)

    if db_data is None:
        db_instance = None
    else:
        db_instance = deserialize_language_certificate(data=db_data)

    update_common_chart(Chart.ChartTitle.DUOLINGO, form_models.DuolingoCertificate,
                        form_models.DuolingoCertificate.get_store_label, instance, db_instance, is_delete)


def update_common_chart(chart_title, instance_model, label_function, instance, db_instance, is_delete=False):
    chart, created = Chart.objects.get_or_create(title=chart_title)

    if is_delete:
        label = label_function(instance)
        with transaction.atomic():
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                               defaults={'count': 0})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)

    else:
        # Save has been called in order to update an entry
        if db_instance is not None:
            old_label = label_function(db_instance)
            new_label = label_function(instance)
            if new_label != old_label:
                with transaction.atomic():
                    obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                                       defaults={'count': 0})
                    if not created:
                        ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)

                with transaction.atomic():
                    obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                                       defaults={'count': 1})
                    if not created:
                        ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)

        # Save has been called in order to create an entry
        else:
            label = label_function(instance)
            with transaction.atomic():
                obj, created = ChartItemData.objects.get_or_create(chart_id=chart.id, label=label,
                                                                   defaults={'count': 1})
                if not created:
                    ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)


@shared_task
def update_chart_by_label(chart_data, new_label, old_label, is_delete=False):
    des_obj = next(deserialize('json', chart_data))
    chart = des_obj.object

    if new_label is not None:
        with transaction.atomic():
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                               defaults={'count': 1})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)

    if old_label is not None:
        with transaction.atomic():
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                               defaults={'count': 0})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)
