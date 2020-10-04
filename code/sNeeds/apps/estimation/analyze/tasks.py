from celery import shared_task, task
from django.core.serializers import deserialize

from django.db.models import Sum, F
from django.db import transaction
from django.db.utils import IntegrityError

from sNeeds.apps.estimation.form import models as account_models
from sNeeds.apps.estimation.analyze.models import Chart, ChartItemData
from sNeeds.apps.estimation.form.serializers import StudentDetailedInfoSerializer


# @shared_task
# def recreate_grade_point_average_all_data():
#     item_range = 0.25
#     sdi_qs = account_models.StudentDetailedInfo.objects.all()
#     educations = account_models.UniversityThrough.objects.none()
#     for sdi in sdi_qs:
#         try:
#             educations |= account_models.UniversityThrough.objects.filter(student_detailed_info=sdi). \
#                 order_by('-graduate_in').first()
#         except account_models.UniversityThrough.DoesNotExist:
#             pass
#
#     data = dict()
#
#     educations = educations.annotate(item_label=Floor(F('gpa') / item_range) * item_range)
#
#     for obj in educations:
#         # item_label = str(math.floor(obj.gpa / item_range) * item_range)
#         data[obj.item_label] = data.get(obj.item_label, 0) + 1
#
#     analyze_models.GradePointAverageChart.objects.all().delete()
#     grade_point_average_chart = analyze_models.GradePointAverageChart.objects.create()
#     for label, count in data.items():
#         ChartItemData.objects.create(chart=grade_point_average_chart, label=label, count=count)


# @shared_task
# def recreate_gre_general_chart():
#     item_range = 0.5
#     qs = account_models.GREGeneralCertificate.objects.all()
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


# @shared_task
# def recreate_powerful_recommendation_number_chart():
#     qs = account_models.StudentDetailedInfo.objects.all()
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


# @shared_task
# def recreate_publication_count_chart():
#     qs = account_models.StudentDetailedInfo.objects.all()
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


@shared_task
def update_publication_count_chart(publications_count, data, db_data, is_delete=False):
    """
    this function for delete signal should be called in post_delete
    :return:
    """

    # print("entered update_publication_count_chart")

    # print(publications_count)

    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitleChoices.PUBLICATIONS_COUNT)

    if is_delete:
        # We check that the instance is the last publication is being removed from sdi publications set
        # publications_count = instance.student_detailed_info.studentdetailedinfo.publication_set.count()
        # print("entered is delete")
        # print(publications_count)

        # sdi_deletion = False
        # print(publications_count)
        # if publications_count == 0:
        #     try:
        #         account_models.StudentDetailedInfo.objects.get(id=instance.student_detailed_info.id)
        #         print("not sdi deletion")
        #     except account_models.StudentDetailedInfo.DoesNotExist:
        #         sdi_deletion = True
        #         print("sdi deletion")
        #
        # return

        old_label = str(publications_count + 1)

        with transaction.atomic():
            # print("old1")
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                               defaults={'count': 0})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)
            # print("old2")

        if publications_count < 0:
            raise Exception("Error in publication count label calculation. Below zero label produced.")

        new_label = str(publications_count)
        with transaction.atomic():
            # print("new1")
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                               defaults={'count': 1})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)

            # print("new2")

    else:
        # Save has been called in order to update an entry
        if db_instance is not None:
            pass
        # Save has been called in order to create an entry
        else:
            # publications_count = instance.student_detailed_info.studentdetailedinfo.publication_set.count()

            # print("entered create mode")

            old_label = str(publications_count)
            # print(old_label)

            with transaction.atomic():
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                                   defaults={'count': 0})
                if not created:
                    ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)

            new_label = str(publications_count + 1)
            # print(new_label)

            with transaction.atomic():
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                                   defaults={'count': 1})
                if not created:
                    ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)


@shared_task
def update_publication_count_chart_sdi_creation(data, db_data, is_delete=False):
    # print("entered sdi creation")
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitleChoices.PUBLICATIONS_COUNT)

    # Save has been called in order to update an entry
    if db_instance is not None:
        pass
    # Save has been called in order to create an entry
    else:
        # publications_count = instance.publication_set.count()
        #
        # if publications_count > 0:
        #     return
        #
        # label = str(publications_count)

        label = '0'

        with transaction.atomic():
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                               defaults={'count': 1})
            if not created:
                ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)


@shared_task
def update_publication_count_chart_sdi_deletion(publications_count, data, db_data, is_delete=False):
    # print(" entered sdi deletion")
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitleChoices.PUBLICATIONS_COUNT)

    if is_delete:
        # publications_count = instance.publication_set.count()

        label = str(publications_count)
        # print(label)

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

    update_common_chart(Chart.ChartTitleChoices.PUBLICATIONS_TYPE, account_models.Publication,
                        account_models.Publication.get_type__store_label, instance, db_instance, is_delete)

    # try:
    #     chart = analyze_models.PublicationTypeCountChart.objects.all().first()
    # except analyze_models.PublicationTypeCountChart.DoesNotExist:
    #     chart = analyze_models.PublicationTypeCountChart.objects.create()
    #
    # if chart is None:
    #     chart = analyze_models.PublicationTypeCountChart.objects.create()
    # # chart = analyze_models.IeltsChart.objects.get_or_create()
    #
    # if is_delete:
    #     # We check that the instance is the last publication is being removed from sdi publications set
    #     label = get_publication_instance_type_label(instance)
    #     with transaction.atomic():
    #             obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                       defaults={'count': 0})
    #     if not created :
    #         obj.count -= 1
    #         obj.save()
    #
    # else:
    #     # Save has been called in order to update an entry
    #     try:
    #         db_instance = account_models.Publication.objects.get(pk=instance.pk)
    #         old_label = get_publication_instance_type_label(db_instance)
    #         new_label = get_publication_instance_type_label(instance)
    #
    #         if new_label != old_label:
    #             with transaction.atomic():
    #              obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
    #                                                                               defaults={'count': 0})
    #             if not created :
    #                 obj.count -= 1
    #                 obj.save()
    #
    #             with transaction.atomic():
    #             obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
    #                                                                               defaults={'count': 1})
    #             if not created:
    #                 obj.count += 1
    #                 obj.save()
    #
    #     except IntegrityError:
    #         pass
    #     # Save has been called in order to create an entry
    #     except account_models.Publication.DoesNotExist or AttributeError:
    #         label = get_publication_instance_type_label(instance)
    #
    #         with transaction.atomic():
    #             obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                           defaults={'count': 1})
    #         if not created:
    #             obj.count += 1
    #             obj.save()


@shared_task
def update_publications_score_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object

    get_publications_score_label = account_models.Publication.get_publications_score__store_label
    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitleChoices.PUBLICATIONS_SCORE)

    if is_delete:
        old_publications_values = instance.student_detailed_info.studentdetailedinfo.publication_set. \
            aggregate(Sum('value')).get('value__sum')
        new_publications_values = old_publications_values - instance.value

        old_label = get_publications_score_label(old_publications_values)
        new_label = get_publications_score_label(new_publications_values)

        if old_label != new_label:
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

    else:
        # Save has been called in order to update an entry
        if db_instance is not None:
            old_publications_values = instance.student_detailed_info.studentdetailedinfo.publication_set \
                .aggregate(Sum('value')).get('value__sum')
            diff = instance.value - db_instance.value
            new_publications_values = old_publications_values + diff

            old_label = get_publications_score_label(old_publications_values)
            new_label = get_publications_score_label(new_publications_values)

            if old_label != new_label:
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
            old_publications_values = instance.student_detailed_info.studentdetailedinfo.publication_set \
                .aggregate(Sum('value')).get('value__sum')
            new_publications_values = old_publications_values + instance.value

            old_label = get_publications_score_label(old_publications_values)
            new_label = get_publications_score_label(new_publications_values)

            if old_label != new_label:
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


@shared_task
def update_powerful_recommendation_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    update_common_chart(Chart.ChartTitleChoices.POWERFUL_RECOMMENDATION, account_models.StudentDetailedInfo,
                        account_models.StudentDetailedInfo.get_powerful_recommendation__store_label,
                        instance, db_instance, is_delete)

    # try:
    #     chart = analyze_models.PowerfulRecommendationCountChart.objects.all().first()
    # except analyze_models.PowerfulRecommendationCountChart.DoesNotExist:
    #     chart = analyze_models.PowerfulRecommendationCountChart.objects.create()
    #
    # if chart is None:
    #     chart = analyze_models.PowerfulRecommendationCountChart.objects.create()
    # # chart = analyze_models.IeltsChart.objects.get_or_create()
    #
    # if is_delete:
    #     label = get_sdi_instance_powerful_recommendation_label(instance)
    #     with transaction.atomic():
    #                 obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                       defaults={'count': 0})
    #     if not created :
    #         obj.count -= 1
    #         obj.save()
    #
    # else:
    #     # Save has been called in order to update an entry
    #     try:
    #         db_instance = account_models.StudentDetailedInfo.objects.get(pk=instance.pk)
    #         old_label = get_sdi_instance_powerful_recommendation_label(db_instance)
    #         new_label = get_sdi_instance_powerful_recommendation_label(instance)
    #
    #         if new_label != old_label:
    #             with transaction.atomic():
    #                 obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
    #                                                                               defaults={'count': 0})
    #             if not created :
    #                 obj.count -= 1
    #                 obj.save()
    #
    #             with transaction.atomic():
    #                 obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
    #                                                                               defaults={'count': 1})
    #             if not created:
    #                 obj.count += 1
    #                 obj.save()
    #     except IntegrityError:
    #         pass
    #     # Save has been called in order to create an entry
    #     except account_models.StudentDetailedInfo.DoesNotExist or AttributeError:
    #         label = get_sdi_instance_powerful_recommendation_label(instance)
    #         with transaction.atomic():
    #                 obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                           defaults={'count': 1})
    #         if not created:
    #             obj.count += 1
    #             obj.save()


@shared_task
def update_olympiad_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    print('task self.olympiad', instance.olympiad)

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    update_common_chart(Chart.ChartTitleChoices.OLYMPIAD, account_models.StudentDetailedInfo,
                        account_models.StudentDetailedInfo.get_olympiad__store_label, instance, db_instance, is_delete)

    # try:
    #     chart = analyze_models.OlympiadCountChart.objects.all().first()
    # except analyze_models.OlympiadCountChart.DoesNotExist:
    #     chart = analyze_models.OlympiadCountChart.objects.create()
    #
    # if chart is None:
    #     chart = analyze_models.OlympiadCountChart.objects.create()
    # # chart = analyze_models.IeltsChart.objects.get_or_create()
    #
    # if is_delete:
    #     label = get_sdi_instance_olympiad_label(instance)
    #     with transaction.atomic():
    #                 obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                       defaults={'count': 0})
    #     if not created :
    #         obj.count -= 1
    #         obj.save()
    #
    # else:
    #     # Save has been called in order to update an entry
    #     try:
    #         db_instance = account_models.StudentDetailedInfo.objects.get(pk=instance.pk)
    #         old_label = get_sdi_instance_olympiad_label(db_instance)
    #         new_label = get_sdi_instance_olympiad_label(instance)
    #
    #         if new_label != old_label:
    #             with transaction.atomic():
    #                 obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
    #                                                                               defaults={'count': 0})
    #             if not created :
    #                 obj.count -= 1
    #                 obj.save()
    #
    #             with transaction.atomic():
    #                 obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
    #                                                                               defaults={'count': 1})
    #             if not created:
    #                 obj.count += 1
    #                 obj.save()
    #     except IntegrityError:
    #         pass
    #     # Save has been called in order to create an entry
    #     except account_models.StudentDetailedInfo.DoesNotExist or AttributeError:
    #         label = get_sdi_instance_olympiad_label(instance)
    #         with transaction.atomic():
    #                 obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                           defaults={'count': 1})
    #         if not created:
    #             obj.count += 1
    #             obj.save()


@shared_task
def update_related_work_experience_chart(data, db_data, is_delete=False):
    # des_obj = next(deserialize('json', data))
    # instance = des_obj.object

    # ser = StudentDetailedInfoTaskSerializer(data=data)
    # ser.is_valid()
    # instance = ser.create(ser.validated_data)

    instance = account_models.StudentDetailedInfo(**data)

    print('task rel work', instance)

    if db_data is None:
        db_instance = None
    else:
        # des_db_obj = next(deserialize('json', db_data))
        # db_instance = des_db_obj.object
        ser = StudentDetailedInfoSerializer(db_data=data)
        ser.is_valid()
        db_instance = ser.create(ser.validated_data)

    print('task self.related_work_experience', instance.related_work_experience)

    update_common_chart(Chart.ChartTitleChoices.RELATED_WORK_EXPERIENCE, account_models.StudentDetailedInfo,
                        account_models.StudentDetailedInfo.get_related_work__store_label, instance, db_instance,
                        is_delete)


@shared_task
def update_publication_impact_factor_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    update_common_chart(Chart.ChartTitleChoices.PUBLICATIONS_IMPACT_FACTOR, account_models.Publication,
                        account_models.Publication.get_impact_factor__store_label, instance, db_instance, is_delete)


@shared_task
def update_gpa_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object

    chart, created = Chart.objects.get_or_create(title=Chart.ChartTitleChoices.GRADE_POINT_AVERAGE)

    if is_delete:
        # We check that the instance is the last education is being removed from sdi educations set
        qs = account_models.UniversityThrough.objects.filter(student_detailed_info=instance.student_detailed_info). \
            order_by('-graduate_in')
        last_grade = qs.first()
        if last_grade == instance:
            label = account_models.UniversityThrough.get_gpa__store_label(last_grade)
            with transaction.atomic():
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                                   defaults={'count': 0})
                if not created:
                    ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)

            # now we look for last grade after instance
            new_last_grade = qs.exclude(pk=instance.pk).first()
            if new_last_grade is not None:
                label = account_models.UniversityThrough.get_gpa__store_label(new_last_grade)
                with transaction.atomic():
                    obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                                       defaults={'count': 1})
                    if not created:
                        ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)

    else:
        # Save has been called in order to update an entry
        if db_instance is not None:
            qs = account_models.UniversityThrough.objects.filter(
                student_detailed_info=instance.student_detailed_info
            ).order_by('-graduate_in')

            is_chart_updated = False

            last_grade = qs.first()
            next_last_grade = qs.exclude(pk=instance.pk).first()

            if instance.pk == last_grade.pk:
                # we check that the instance graduate has changed and is not going to be the last grade any more
                if instance.graduate_in < last_grade.graduate_in \
                        and next_last_grade is not None and instance.graduate_in < next_last_grade.graduate_in:

                    label = account_models.UniversityThrough.get_gpa__store_label(last_grade)
                    with transaction.atomic():
                        obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                                           defaults={'count': 0})
                        if not created:
                            ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)

                    label = account_models.UniversityThrough.get_gpa__store_label(next_last_grade)
                    with transaction.atomic():
                        obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                                           defaults={'count': 1})
                        if not created:
                            ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)

                    is_chart_updated = True

                # We check gpa changes. If we do not enter the previous if statement it means the instance still is
                # last grade.We check that by is_chart_updated flag.
                if instance.gpa != db_instance.gpa and not is_chart_updated:
                    old_label = account_models.UniversityThrough.get_gpa__store_label(db_instance)
                    new_label = account_models.UniversityThrough.get_gpa__store_label(instance)
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

            # The instance was not last grade education but maybe it become last grade by increasing graduate_in value!
            elif instance.graduate_in > last_grade.graduate_in:
                old_label = account_models.UniversityThrough.get_gpa__store_label(last_grade)
                with transaction.atomic():
                    obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                                       defaults={'count': 0})
                    if not created:
                        ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)

                new_label = account_models.UniversityThrough.get_gpa__store_label(instance)
                with transaction.atomic():
                    obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                                       defaults={'count': 1})
                    if not created:
                        ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)

        # Save has been called in order to create an entry
        else:
            qs = account_models.UniversityThrough.objects.filter(
                student_detailed_info=instance.student_detailed_info
            ).order_by('-graduate_in')

            last_grade = qs.first()

            if last_grade is None:
                label = account_models.UniversityThrough.get_gpa__store_label(instance)
                with transaction.atomic():
                    obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                                       defaults={'count': 1})
                    if not created:
                        ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)

            elif instance.graduate_in > last_grade.graduate_in:
                old_label = account_models.UniversityThrough.get_gpa__store_label(last_grade)
                with transaction.atomic():
                    obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                                       defaults={'count': 0})
                    if not created:
                        ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') - 1)

                new_label = account_models.UniversityThrough.get_gpa__store_label(instance)
                with transaction.atomic():
                    obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                                       defaults={'count': 1})
                    if not created:
                        ChartItemData.objects.filter(pk=obj.pk).update(count=F('count') + 1)


@shared_task
def update_language_certificates_charts(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if instance.is_mock:
        return

    if instance.certificate_type == account_models.LanguageCertificateType.IELTS_GENERAL or \
            instance.certificate_type == account_models.LanguageCertificateType.IELTS_ACADEMIC:
        update_ielts_chart(data=data, db_data=db_data, is_delete=is_delete)

    elif instance.certificate_type == account_models.LanguageCertificateType.TOEFL:
        update_toefl_chart(data=data, db_data=db_data, is_delete=is_delete)

    elif instance.certificate_type == account_models.LanguageCertificateType.GMAT:
        update_gmat_chart(data=data, db_data=db_data, is_delete=is_delete)

    elif instance.certificate_type == account_models.LanguageCertificateType.GRE_GENERAL:
        update_gre_general_writing_chart(data=data, db_data=db_data, is_delete=is_delete)
        update_gre_general_quantitative_and_verbal_chart(data=data, db_data=db_data, is_delete=is_delete)

    elif instance.certificate_type == account_models.LanguageCertificateType.GRE_MATHEMATICS or \
            instance.certificate_type == account_models.LanguageCertificateType.GRE_CHEMISTRY or \
            instance.certificate_type == account_models.LanguageCertificateType.GRE_LITERATURE or \
            instance.certificate_type == account_models.LanguageCertificateType.GRE_PHYSICS or \
            instance.certificate_type == account_models.LanguageCertificateType.GRE_BIOLOGY or \
            instance.certificate_type == account_models.LanguageCertificateType.GRE_PSYCHOLOGY:
        update_gre_subject_total_chart(data=data, db_data=db_data, is_delete=is_delete)

    elif instance.certificate_type == account_models.LanguageCertificateType.DUOLINGO:
        update_duolingo_chart(data=data, db_data=db_data, is_delete=is_delete)

    # elif instance.certificate_type == account_models.LanguageCertificateType.GRE_PHYSICS:
    #     update_gre_physics_chart(instance=instance, is_delete=is_delete)
    #
    # elif instance.certificate_type == account_models.LanguageCertificateType.GRE_BIOLOGY:
    #     update_gre_biology_chart(instance=instance, is_delete=is_delete)
    #
    # elif instance.certificate_type == account_models.LanguageCertificateType.GRE_PSYCHOLOGY:
    #     update_gre_psychology_chart(instance=instance, is_delete=is_delete)


def update_ielts_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    # instance = instance.regularlanguagcertificate
    update_common_chart(Chart.ChartTitleChoices.IELTS, account_models.RegularLanguageCertificate,
                        account_models.RegularLanguageCertificate.get_ielts__store_label,
                        instance, is_delete)


def update_toefl_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    # instance = instance.regularlanguagcertificate
    update_common_chart(Chart.ChartTitleChoices.TOEFL, account_models.RegularLanguageCertificate,
                        account_models.RegularLanguageCertificate.get_toefl__store_label,
                        instance, is_delete)


def update_gmat_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    # instance = instance.gmatcertificate
    update_common_chart(Chart.ChartTitleChoices.GMAT, account_models.GMATCertificate,
                        account_models.GMATCertificate.get_store_label,
                        instance, is_delete)


def update_gre_general_writing_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    # instance = instance.gregeneralcertificate
    update_common_chart(Chart.ChartTitleChoices.GRE_GENERAL_WRITING, account_models.GREGeneralCertificate,
                        account_models.GREGeneralCertificate.get_writing_store_label, instance, db_instance, is_delete)


def update_gre_general_quantitative_and_verbal_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    # instance = instance.gregeneralcertificate
    update_common_chart(Chart.ChartTitleChoices.GRE_GENERAL_QUANTITATIVE_AND_VERBAL, account_models.GREGeneralCertificate,
                        account_models.GREGeneralCertificate.get_q_and_v_store_label, instance, db_instance, is_delete)


def update_gre_subject_total_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    # instance = instance.gresubjectcertificate
    update_common_chart(Chart.ChartTitleChoices.GRE_SUBJECT_TOTAL, account_models.GRESubjectCertificate,
                        account_models.GRESubjectCertificate.get_total_store_label, instance, db_instance, is_delete)


def update_duolingo_chart(data, db_data, is_delete=False):
    des_obj = next(deserialize('json', data))
    instance = des_obj.object

    if db_data is None:
        db_instance = None
    else:
        des_db_obj = next(deserialize('json', db_data))
        db_instance = des_db_obj.object
    # instance = instance.duolingocertificate
    update_common_chart(Chart.ChartTitleChoices.DUOLINGO, account_models.DuolingoCertificate,
                        account_models.DuolingoCertificate.get_store_label, instance, db_instance, is_delete)


def update_common_chart(chart_title, instance_model, label_function, instance, db_instance, is_delete=False):
    chart, created = Chart.objects.get_or_create(title=chart_title)

    # print(chart)
    # print(type(chart))

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
