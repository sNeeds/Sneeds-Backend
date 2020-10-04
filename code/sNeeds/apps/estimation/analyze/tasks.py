from celery import shared_task

from django.db.models import Sum
from django.db.utils import IntegrityError

import sNeeds.apps.estimation.form.models
from sNeeds.apps.data.account import models as account_models
from sNeeds.apps.estimation.analyze import Chart, ChartTitle, ChartItemData


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
def update_publication_count_chart(instance, is_delete=False):
    chart = Chart.objects.get_or_create(title=ChartTitle.PUBLICATIONS_COUNT.value)

    if is_delete:
        # We check that the instance is the last publication is being removed from sdi publications set
        try:
            publications_count = instance.student_detailed_info.publication_set.count()
        except Exception:
            return
        old_label = str(publications_count)
        obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                           defaults={'count': 0})
        if not created and obj.count > 0:
            obj.count -= 1
            obj.save()

        publications_count -= 1
        if publications_count < 0:
            raise Exception("Error in publication count label calculation. Below zero label produced.")
        new_label = str(publications_count)
        obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                           defaults={'count': 1})
        if not created:
            obj.count += 1
            obj.save()

    else:
        # Save has been called in order to update an entry
        try:
            db_instance = sNeeds.apps.estimation.form.models.Publication.objects.get(pk=instance.pk)
        except IntegrityError:
            pass
        # Save has been called in order to create an entry
        except sNeeds.apps.estimation.form.models.Publication.DoesNotExist or AttributeError:
            publications_count = instance.student_detailed_info.publication_set.count()

            old_label = str(publications_count)
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                               defaults={'count': 0})
            if not created and obj.count > 0:
                obj.count -= 1
                obj.save()

            publications_count += 1
            new_label = str(publications_count)

            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                               defaults={'count': 1})
            if not created:
                obj.count += 1
                obj.save()


@shared_task
def update_publication_count_chart_sdi_creation(instance, is_delete=False):
    chart = Chart.objects.get_or_create(title=ChartTitle.PUBLICATIONS_COUNT.value)

    # Save has been called in order to update an entry
    try:
        db_instance = sNeeds.apps.estimation.form.models.StudentDetailedInfo.objects.get(pk=instance.pk)
    except IntegrityError:
        pass
    # Save has been called in order to create an entry
    except sNeeds.apps.estimation.form.models.StudentDetailedInfo.DoesNotExist or AttributeError:
        publications_count = instance.publication_set.count()

        if publications_count > 0:
            return

        label = str(publications_count)

        obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                           defaults={'count': 1})
        if not created:
            obj.count += 1
            obj.save()


@shared_task
def update_publication_count_chart_sdi_deletion(instance, is_delete=False):
    chart = Chart.objects.get_or_create(title=ChartTitle.PUBLICATIONS_COUNT.value)

    if is_delete:
        publications_count = instance.publication_set.count()

        label = str(publications_count)

        obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                           defaults={'count': 0})
        if not created and obj.count > 0:
            obj.count -= 1
            obj.save()


@shared_task
def update_publication_type_count_chart(instance, is_delete=False):
    update_common_chart(ChartTitle.PUBLICATIONS_TYPE.value, sNeeds.apps.estimation.form.models.Publication,
                        sNeeds.apps.estimation.form.models.Publication.get_type__store_label, instance, is_delete)

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
    #     obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                       defaults={'count': 0})
    #     if not created and obj.count > 0:
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
    #             obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
    #                                                                               defaults={'count': 0})
    #             if not created and obj.count > 0:
    #                 obj.count -= 1
    #                 obj.save()
    #
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
    #         obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                           defaults={'count': 1})
    #         if not created:
    #             obj.count += 1
    #             obj.save()


@shared_task
def update_powerful_recommendation_count_chart(instance, is_delete=False):
    update_common_chart(ChartTitle.POWERFUL_RECOMMENDATION.value,
                        sNeeds.apps.estimation.form.models.StudentDetailedInfo,
                        sNeeds.apps.estimation.form.models.StudentDetailedInfo.get_powerful_recommendation__store_label,
                        instance, is_delete)

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
    #     obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                       defaults={'count': 0})
    #     if not created and obj.count > 0:
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
    #             obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
    #                                                                               defaults={'count': 0})
    #             if not created and obj.count > 0:
    #                 obj.count -= 1
    #                 obj.save()
    #
    #             obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
    #                                                                               defaults={'count': 1})
    #             if not created:
    #                 obj.count += 1
    #                 obj.save()
    #     except IntegrityError:
    #         pass
    #     # Save has been called in order to create an entry
    #     except account_models.StudentDetailedInfo.DoesNotExist or AttributeError:
    #         label = get_sdi_instance_powerful_recommendation_label(instance)
    #         obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                           defaults={'count': 1})
    #         if not created:
    #             obj.count += 1
    #             obj.save()


@shared_task
def update_publications_score_chart(instance, is_delete=False):
    get_publications_score_label = sNeeds.apps.estimation.form.models.Publication.get_publications_score__store_label
    chart = Chart.objects.get_or_create(title=ChartTitle.PUBLICATIONS_SCORE.value)

    if is_delete:
        old_publications_values = instance.student_detailed_info.publication_set. \
            aggregate(Sum('value')).get('value__sum')
        new_publications_values = old_publications_values - instance.value

        old_label = get_publications_score_label(old_publications_values)
        new_label = get_publications_score_label(new_publications_values)

        if old_label != new_label:
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                               defaults={'count': 0})
            if not created and obj.count > 0:
                obj.count -= 1
                obj.save()

            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                               defaults={'count': 1})
            if not created:
                obj.count += 1
                obj.save()

    else:
        # Save has been called in order to update an entry
        try:
            db_instance = sNeeds.apps.estimation.form.models.Publication.objects.get(pk=instance.pk)
            old_publications_values = instance.student_detailed_info.publication_set \
                .aggregate(Sum('value')).get('value__sum')
            diff = instance.value - db_instance.value
            new_publications_values = old_publications_values + diff

            old_label = get_publications_score_label(old_publications_values)
            new_label = get_publications_score_label(new_publications_values)

            if old_label != new_label:
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                                   defaults={'count': 0})
                if not created and obj.count > 0:
                    obj.count -= 1
                    obj.save()

                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                                   defaults={'count': 1})
                if not created:
                    obj.count += 1
                    obj.save()
        except IntegrityError:
            pass
        # Save has been called in order to create an entry
        except sNeeds.apps.estimation.form.models.Publication.DoesNotExist or AttributeError:
            old_publications_values = instance.student_detailed_info.publication_set \
                .aggregate(Sum('value')).get('value__sum')
            new_publications_values = old_publications_values + instance.value

            old_label = get_publications_score_label(old_publications_values)
            new_label = get_publications_score_label(new_publications_values)

            if old_label != new_label:
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                                   defaults={'count': 0})
                if not created and obj.count > 0:
                    obj.count -= 1
                    obj.save()

                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                                   defaults={'count': 1})
                if not created:
                    obj.count += 1
                    obj.save()


@shared_task
def update_olympiad_count_chart(instance, is_delete=False):
    update_common_chart(ChartTitle.OLYMPIAD.value, sNeeds.apps.estimation.form.models.StudentDetailedInfo,
                        sNeeds.apps.estimation.form.models.StudentDetailedInfo.get_olympiad__store_label, instance, is_delete)

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
    #     obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                       defaults={'count': 0})
    #     if not created and obj.count > 0:
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
    #             obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
    #                                                                               defaults={'count': 0})
    #             if not created and obj.count > 0:
    #                 obj.count -= 1
    #                 obj.save()
    #
    #             obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
    #                                                                               defaults={'count': 1})
    #             if not created:
    #                 obj.count += 1
    #                 obj.save()
    #     except IntegrityError:
    #         pass
    #     # Save has been called in order to create an entry
    #     except account_models.StudentDetailedInfo.DoesNotExist or AttributeError:
    #         label = get_sdi_instance_olympiad_label(instance)
    #         obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
    #                                                                           defaults={'count': 1})
    #         if not created:
    #             obj.count += 1
    #             obj.save()


@shared_task
def update_related_work_experience_chart(instance, is_delete=False):
    update_common_chart(ChartTitle.RELATED_WORK_EXPERIENCE.value,
                        sNeeds.apps.estimation.form.models.StudentDetailedInfo,
                        sNeeds.apps.estimation.form.models.StudentDetailedInfo.get_related_work__store_label, instance, is_delete)


@shared_task
def update_publication_impact_factor_chart(instance, is_delete=False):
    update_common_chart(ChartTitle.PUBLICATIONS_IMPACT_FACTOR.value,
                        sNeeds.apps.estimation.form.models.Publication,
                        sNeeds.apps.estimation.form.models.Publication.get_impact_factor__store_label, instance, is_delete)


@shared_task
def update_gpa_chart(instance, is_delete=False):
    chart = Chart.objects.get(title=ChartTitle.GRADE_POINT_AVERAGE.value)
    # chart = analyze_models.IeltsChart.objects.get_or_create()
    if is_delete:
        # We check that the instance is the last education is being removed from sdi educations set
        qs = sNeeds.apps.estimation.form.models.UniversityThrough.objects.filter(student_detailed_info=instance.student_detailed_info). \
            order_by('-graduate_in')
        last_grade = qs.first()
        if last_grade == instance:
            label = sNeeds.apps.estimation.form.models.UniversityThrough.get_gpa__store_label(last_grade)
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                               defaults={'count': 0})
            if not created and obj.count > 0:
                obj.count -= 1
                obj.save()

            # now we look for last grade after instance
            new_last_grade = qs.exclude(pk=instance.pk).first()
            if new_last_grade is not None:
                label = sNeeds.apps.estimation.form.models.UniversityThrough.get_gpa__store_label(new_last_grade)
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                                   defaults={'count': 1})
                if not created:
                    obj.count += 1
                    obj.save()

    else:
        # Save has been called in order to update an entry
        try:
            db_instance = sNeeds.apps.estimation.form.models.UniversityThrough.objects.get(pk=instance.pk)
            qs = sNeeds.apps.estimation.form.models.UniversityThrough.objects.filter(
                student_detailed_info=instance.student_detailed_info
            ).order_by('-graduate_in')

            is_chart_updated = False

            last_grade = qs.first()
            next_last_grade = qs.exclude(pk=instance.pk).first()

            if instance.pk == last_grade.pk:
                # we check that the instance graduate has changed and is not going to be the last grade any more
                if instance.graduate_in < last_grade.graduate_in \
                        and next_last_grade is not None and instance.graduate_in < next_last_grade.graduate_in:

                    label = sNeeds.apps.estimation.form.models.UniversityThrough.get_gpa__store_label(last_grade)
                    obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                                       defaults={'count': 0})
                    if not created and obj.count > 0:
                        obj.count -= 1
                        obj.save()

                    label = sNeeds.apps.estimation.form.models.UniversityThrough.get_gpa__store_label(next_last_grade)
                    obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                                       defaults={'count': 1})
                    if not created:
                        obj.count += 1
                        obj.save()

                    is_chart_updated = True

                # We check gpa changes. If we do not enter the previous if statement it means the instance still is
                # last grade.We check that by is_chart_updated flag.
                if instance.gpa != db_instance.gpa and not is_chart_updated:
                    old_label = sNeeds.apps.estimation.form.models.UniversityThrough.get_gpa__store_label(db_instance)
                    new_label = sNeeds.apps.estimation.form.models.UniversityThrough.get_gpa__store_label(instance)
                    if new_label != old_label:
                        obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                                           defaults={'count': 0})
                        if not created and obj.count > 0:
                            obj.count -= 1
                            obj.save()

                        obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                                           defaults={'count': 1})
                        if not created:
                            obj.count += 1
                            obj.save()

            # The instance was not last grade education but maybe it become last grade by increasing graduate_in value!
            elif instance.graduate_in > last_grade.graduate_in:
                old_label = sNeeds.apps.estimation.form.models.UniversityThrough.get_gpa__store_label(last_grade)
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                                   defaults={'count': 0})
                if not created and obj.count > 0:
                    obj.count -= 1
                    obj.save()

                new_label = sNeeds.apps.estimation.form.models.UniversityThrough.get_gpa__store_label(instance)
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                                   defaults={'count': 1})
                if not created:
                    obj.count += 1
                    obj.save()

        except IntegrityError:
            pass
        # Save has been called in order to create an entry
        except sNeeds.apps.estimation.form.models.UniversityThrough.DoesNotExist or AttributeError:
            qs = sNeeds.apps.estimation.form.models.UniversityThrough.objects.filter(
                student_detailed_info=instance.student_detailed_info
            ).order_by('-graduate_in')

            last_grade = qs.first()

            if last_grade is None:
                label = sNeeds.apps.estimation.form.models.UniversityThrough.get_gpa__store_label(instance)
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                                   defaults={'count': 1})
                if not created:
                    obj.count += 1
                    obj.save()

            elif instance.graduate_in > last_grade.graduate_in:
                old_label = sNeeds.apps.estimation.form.models.UniversityThrough.get_gpa__store_label(last_grade)
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                                   defaults={'count': 0})
                if not created and obj.count > 0:
                    obj.count -= 1
                    obj.save()

                new_label = sNeeds.apps.estimation.form.models.UniversityThrough.get_gpa__store_label(instance)
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                                   defaults={'count': 1})
                if not created:
                    obj.count += 1
                    obj.save()


@shared_task
def update_language_certificates_charts(instance, is_delete=False):
    if instance.is_mock:
        return

    if instance.certificate_type == account_models.LanguageCertificateType.IELTS_GENERAL or \
            instance.certificate_type == account_models.LanguageCertificateType.IELTS_ACADEMIC:
        update_ielts_chart(instance=instance, is_delete=is_delete)

    elif instance.certificate_type == account_models.LanguageCertificateType.TOEFL:
        update_toefl_chart(instance=instance, is_delete=is_delete)

    elif instance.certificate_type == account_models.LanguageCertificateType.GMAT:
        update_gmat_chart(instance=instance, is_delete=is_delete)

    elif instance.certificate_type == account_models.LanguageCertificateType.GRE_GENERAL:
        update_gre_general_writing_chart(instance=instance, is_delete=is_delete)
        update_gre_general_quantitative_and_verbal_chart(instance=instance, is_delete=is_delete)

    elif instance.certificate_type == account_models.LanguageCertificateType.GRE_MATHEMATICS or \
            instance.certificate_type == account_models.LanguageCertificateType.GRE_CHEMISTRY or \
            instance.certificate_type == account_models.LanguageCertificateType.GRE_LITERATURE or \
            instance.certificate_type == account_models.LanguageCertificateType.GRE_PHYSICS or \
            instance.certificate_type == account_models.LanguageCertificateType.GRE_BIOLOGY or \
            instance.certificate_type == account_models.LanguageCertificateType.GRE_PSYCHOLOGY:
        update_gre_subject_total_chart(instance=instance, is_delete=is_delete)

    elif instance.certificate_type == account_models.LanguageCertificateType.DUOLINGO:
        update_duolingo_chart(instance=instance, is_delete=is_delete)

    # elif instance.certificate_type == account_models.LanguageCertificateType.GRE_PHYSICS:
    #     update_gre_physics_chart(instance=instance, is_delete=is_delete)
    #
    # elif instance.certificate_type == account_models.LanguageCertificateType.GRE_BIOLOGY:
    #     update_gre_biology_chart(instance=instance, is_delete=is_delete)
    #
    # elif instance.certificate_type == account_models.LanguageCertificateType.GRE_PSYCHOLOGY:
    #     update_gre_psychology_chart(instance=instance, is_delete=is_delete)


def update_ielts_chart(instance, is_delete=False):
    # instance = instance.regularlanguagcertificate
    update_common_chart(ChartTitle.IELTS.value, sNeeds.apps.estimation.form.models.RegularLanguageCertificate,
                        sNeeds.apps.estimation.form.models.RegularLanguageCertificate.get_ielts__store_label,
                        instance, is_delete)


def update_toefl_chart(instance, is_delete=False):
    # instance = instance.regularlanguagcertificate
    update_common_chart(ChartTitle.TOEFL.value, sNeeds.apps.estimation.form.models.RegularLanguageCertificate,
                        sNeeds.apps.estimation.form.models.RegularLanguageCertificate.get_toefl__store_label,
                        instance, is_delete)


def update_gmat_chart(instance, is_delete=False):
    # instance = instance.gmatcertificate
    update_common_chart(ChartTitle.GMAT.value, sNeeds.apps.estimation.form.models.GMATCertificate,
                        sNeeds.apps.estimation.form.models.GMATCertificate.get_store_label,
                        instance, is_delete)


def update_gre_general_writing_chart(instance, is_delete=False):
    # instance = instance.gregeneralcertificate
    update_common_chart(ChartTitle.GRE_GENERAL_WRITING.value,
                        sNeeds.apps.estimation.form.models.GREGeneralCertificate,
                        sNeeds.apps.estimation.form.models.GREGeneralCertificate.get_writing_store_label, instance, is_delete)


def update_gre_general_quantitative_and_verbal_chart(instance, is_delete=False):
    # instance = instance.gregeneralcertificate
    update_common_chart(ChartTitle.GRE_GENERAL_QUANTITATIVE_AND_VERBAL.value,
                        sNeeds.apps.estimation.form.models.GREGeneralCertificate,
                        sNeeds.apps.estimation.form.models.GREGeneralCertificate.get_q_and_v_store_label, instance, is_delete)


def update_gre_subject_total_chart(instance, is_delete=False):
    # instance = instance.gresubjectcertificate
    update_common_chart(ChartTitle.GRE_SUBJECT_TOTAL.value,
                        sNeeds.apps.estimation.form.models.GRESubjectCertificate,
                        sNeeds.apps.estimation.form.models.GRESubjectCertificate.get_total_store_label, instance, is_delete)


def update_duolingo_chart(instance, is_delete=False):
    # instance = instance.duolingocertificate
    update_common_chart(ChartTitle.DUOLINGO.value, sNeeds.apps.estimation.form.models.DuolingoCertificate,
                        sNeeds.apps.estimation.form.models.DuolingoCertificate.get_store_label, instance, is_delete)


def update_common_chart(chart_title, instance_model, label_function, instance, is_delete=False):
    chart = Chart.objects.get_or_create(title=chart_title)

    if is_delete:
        label = label_function(instance)
        obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                           defaults={'count': 0})
        if not created and obj.count > 0:
            obj.count -= 1
            obj.save()

    else:
        # Save has been called in order to update an entry
        try:
            db_instance = instance_model.objects.get(pk=instance.pk)
            old_label = label_function(db_instance)
            new_label = label_function(instance)
            if new_label != old_label:
                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=old_label,
                                                                   defaults={'count': 0})
                if not created and obj.count > 0:
                    obj.count -= 1
                    obj.save()

                obj, created = ChartItemData.objects.get_or_create(chart=chart, label=new_label,
                                                                   defaults={'count': 1})
                if not created:
                    obj.count += 1
                    obj.save()

        except IntegrityError:
            pass
        # Save has been called in order to create an entry
        except instance_model.DoesNotExist or AttributeError:
            label = label_function(instance)
            obj, created = ChartItemData.objects.get_or_create(chart=chart, label=label,
                                                               defaults={'count': 1})
            if not created:
                obj.count += 1
                obj.save()
