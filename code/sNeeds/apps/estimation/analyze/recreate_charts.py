# from celery import shared_task
#
# from django.core.serializers import deserialize
# from django.db.models import Sum, F
# from django.db import transaction
#
# from sNeeds.apps.estimation.form import models as form_models
# from sNeeds.apps.estimation.analyze.models import Chart, ChartItemData
# from sNeeds.apps.estimation.form.serializers import StudentDetailedInfoCelerySerializer
#
# LanguageCertificateType = form_models.LanguageCertificate.LanguageCertificateType
#
#
# @shared_task
# def recreate_grade_point_average_all_data():
#     qs = form_models.StudentDetailedInfo.objects.all()
#
#     chart_data = dict()
#     chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.PUBLICATIONS_COUNT)
#     for object in qs:
#
#
#
# @shared_task
# def recreate_gre_general_chart():
#     item_range = 0.5
#     qs = form_models.GREGeneralCertificate.objects.all()
#     data = dict()
#
#     qs = qs.annotate(item_label=Floor(F('overall') / item_range) * item_range)
#
#     for obj in qs:
#         # item_label = str(math.floor(obj.overall / item_range) * item_range)
#         data[obj.item_label] = data.get(obj.item_label, 0) + 1
#
#     analyze_models.IeltsChart.objects.all().delete()
#     ielts_chart = analyze_models.IeltsChart.objects.create()
#     for label, count in data.items():
#         ChartItemData.objects.create(chart=ielts_chart, label=label, count=count)
#
#
# @shared_task
# def recreate_powerful_recommendation_number_chart():
#     qs = form_models.StudentDetailedInfo.objects.all()
#     data = dict()
#
#     for obj in qs:
#         if obj.powerful_recommendation is not None and obj.powerful_recommendation is True:
#             data[REWARDED_LABEL] = data.get(REWARDED_LABEL, 0) + 1
#         else:
#             data[MISSING_LABEL] = data.get(MISSING_LABEL, 0) + 1
#
#     analyze_models.PublicationCountChart.objects.all().delete()
#     chart = analyze_models.IeltsChart.objects.create()
#     for label, count in data.items():
#         ChartItemData.objects.create(chart=chart, label=label, count=count)
#
#
# @shared_task
# def recreate_publication_count_chart():
#     qs = form_models.StudentDetailedInfo.objects.all()
#     data = dict()
#
#     for obj in qs:
#         if obj.publication_set.objects.all().exists():
#             data[REWARDED_LABEL] = data.get(REWARDED_LABEL, 0) + 1
#         else:
#             data[MISSING_LABEL] = data.get(MISSING_LABEL, 0) + 1
#
#     analyze_models.PublicationCountChart.objects.all().delete()
#     chart = analyze_models.IeltsChart.objects.create()
#     for label, count in data.items():
#         ChartItemData.objects.create(chart=chart, label=label, count=count)
#
#
