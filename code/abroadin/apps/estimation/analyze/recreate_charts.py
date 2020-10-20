from celery import shared_task

from django.core.serializers import deserialize
from django.db.models import Sum, F, Count
from django.db import transaction

from abroadin.apps.estimation.form import models as form_models
from abroadin.apps.estimation.analyze.models import Chart, ChartItemData
from abroadin.apps.estimation.form.serializers import StudentDetailedInfoCelerySerializer

LanguageCertificateType = form_models.LanguageCertificate.LanguageCertificateType


# @shared_task
# def recreate_grade_point_average_all_data():
#     qs = form_models.StudentDetailedInfo.objects.all()
#
#     chart_data = dict()
#     chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.PUBLICATIONS_COUNT)
#     for object in qs:


# @shared_task
# def recreate_gre_general_chart():
#     item_range = 0.5
#     qs = form_models.GREGeneralCertificate.objects.all()
#     data = dict()
#
#     qs = qs.annotate(item_label=Floor(F('overall') / item_range) * item_range)

# for obj in qs:
#     # item_label = str(math.floor(obj.overall / item_range) * item_range)
#     data[obj.item_label] = data.get(obj.item_label, 0) + 1
#
# analyze_models.IeltsChart.objects.all().delete()
# ielts_chart = analyze_models.IeltsChart.objects.create()
# for label, count in data.items():
#     ChartItemData.objects.create(chart=ielts_chart, label=label, count=count)


@shared_task
def recreate_student_detailed_info_charts():
    qs = form_models.StudentDetailedInfo.objects.annotate(num_publishes=Count('Publication'))
    powerful_recommendation_data = {}
    olympiad_data = {}
    related_work_data = {}
    publications_count_data = {}

    for obj in qs:
        powerful_recommendation_label = form_models.StudentDetailedInfo.get_powerful_recommendation__store_label(obj)
        powerful_recommendation_data[powerful_recommendation_label] = \
            powerful_recommendation_data.get(powerful_recommendation_label, 0) + 1

        olympiad_label = form_models.StudentDetailedInfo.get_olympiad__store_label(obj)
        olympiad_data[olympiad_label] = olympiad_data.get(olympiad_label, 0) + 1

        related_work_label = form_models.StudentDetailedInfo.get_related_work__store_label(obj)
        related_work_data[related_work_label] = related_work_data.get(related_work_label, 0) + 1

        publications_count_label = str(obj.num_publishes)
        publications_count_data[publications_count_label] = publications_count_data.get(publications_count_label, 0) + 1

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.POWERFUL_RECOMMENDATION)
    for label, count in powerful_recommendation_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.OLYMPIAD)
    for label, count in olympiad_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.RELATED_WORK_EXPERIENCE)
    for label, count in related_work_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.PUBLICATIONS_COUNT)
    for label, count in publications_count_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})


@shared_task
def recreate_publication_charts():
    qs = form_models.Publication.objects.all()
    type_data = {}
    impact_factor_data = {}

    for obj in qs:
        type_label = form_models.Publication.get_type__store_label(obj)
        type_data[type_label] = type_data.get(type_label, 0) + 1

        impact_factor_label = form_models.Publication.get_impact_factor__store_label(obj)
        impact_factor_data[impact_factor_label] = impact_factor_data.get(impact_factor_label, 0) + 1

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.PUBLICATION_TYPE)
    for label, count in type_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.PUBLICATION_IMPACT_FACTOR)
    for label, count in impact_factor_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})


@shared_task
def recreate_regular_language_certificate_chart():
    qs = form_models.RegularLanguageCertificate.objects.all()
    ielts_data = {}
    toefl_data = {}

    for obj in qs:
        if obj.certificate_type == LanguageCertificateType.IELTS_GENERAL or \
                obj.certificate_type == LanguageCertificateType.IELTS_ACADEMIC:
            ielts_label = form_models.RegularLanguageCertificate.get_ielts__store_label(obj)
            ielts_data[ielts_label] = ielts_data.get(ielts_label, 0) + 1

        elif obj.certificate_type == LanguageCertificateType.TOEFL:
            toefl_label = form_models.RegularLanguageCertificate.get_toefl__store_label(obj)
            toefl_data[toefl_label] = toefl_data.get(toefl_label, 0) + 1

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.IELTS)
    for label, count in ielts_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.TOEFL)
    for label, count in toefl_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})


@shared_task
def recreate_gmat_language_certificate_chart():
    qs = form_models.GMATCertificate.objects.all()
    gmat_data = {}

    for obj in qs:
        gmat_label = form_models.GMATCertificate.get_store_label(obj)
        gmat_data[gmat_label] = gmat_data.get(gmat_label, 0) + 1

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.GMAT)
    for label, count in gmat_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})


@shared_task
def recreate_duolingo_language_certificate_chart():
    qs = form_models.DuolingoCertificate.objects.all()
    duolingo_data = {}

    for obj in qs:
        duolingo_label = form_models.DuolingoCertificate.get_store_label(obj)
        duolingo_data[duolingo_label] = duolingo_data.get(duolingo_label, 0) + 1

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.DUOLINGO)
    for label, count in duolingo_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})


@shared_task
def recreate_gre_general_language_certificate_chart():
    qs = form_models.GREGeneralCertificate.objects.all()
    writing_data = {}
    q_and_v_data = {}

    for obj in qs:
        writing_label = form_models.GREGeneralCertificate.get_writing_store_label(obj)
        writing_data[writing_label] = writing_data.get(writing_label, 0) + 1

        q_and_v_label = form_models.GREGeneralCertificate.get_q_and_v_store_label(obj)
        q_and_v_data[q_and_v_label] = q_and_v_data.get(q_and_v_label, 0) + 1

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.GRE_GENERAL_WRITING)
    for label, count in writing_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.GRE_GENERAL_QUANTITATIVE_AND_VERBAL)
    for label, count in q_and_v_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})


@shared_task
def recreate_gre_subject_total_language_certificate_chart():
    qs = form_models.GRESubjectCertificate.objects.all()
    total_score_data = {}

    for obj in qs:
        total_score_label = form_models.GMATCertificate.get_store_label(obj)
        total_score_data[total_score_label] = total_score_data.get(total_score_label, 0) + 1

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.GRE_SUBJECT_TOTAL)
    for label, count in total_score_data.items():
        ChartItemData.objects.update_or_create(chart=chart, label=label, defaults={'count': count})
