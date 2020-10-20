import itertools

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Value, FloatField

from abroadin.apps.users.consultants.models import ConsultantProfile, StudyInfo


def search_consultants(qs, phrase):
    if phrase is None:
        return qs

    vector = SearchVector('user__first_name', weight='B') + SearchVector('user__last_name', weight='B') + \
             SearchVector('bio', weight='B')\
             + SearchVector('studyinfo__university__country__search_name', weight='A')\
             + SearchVector('studyinfo__university__search_name', weight='A')\
             + SearchVector('studyinfo__major__search_name', weight='A')

    query = SearchQuery(phrase, search_type='websearch')
    # ids1 = set(StudyInfo.objects.filter(university__country__search_name__search=phrase).values_list('consultant__id',
    #                                                                                                  flat=True))
    # ids2 = set(StudyInfo.objects.filter(university__search_name__search=phrase).values_list('consultant__id',
    #                                                                                         flat=True))
    # ids3 = set(StudyInfo.objects.filter(major__search_name__search=phrase).values_list('consultant__id',
    #                                                                                    flat=True))
    #
    # ids = ids1 | ids2 | ids3
    #
    # # https://stackoverflow.com/questions/3590306/django-static-annotation
    # queryset1 = ConsultantProfile.objects.filter(id__in=ids, active=True).annotate(rank=Value(0.5, FloatField()))

    # queryset2 = qs.filter(active=True).annotate(
    #     rank=SearchRank(
    #         vector,
    #         query,
    #         normalization=Value(1),
    #     )
    # )

    # print(queryset2)
    # for obj in queryset2:
    #     print(obj.rank)

    # queryset2 = queryset2.filter(rank__gte=0.05)
    #
    # # queryset2 = queryset2.order_by('-rank')
    #
    # # find common objects and delete the object with lower rank from it's queryset
    # # temp_queryset = queryset1 | queryset2
    # temp_queryset = itertools.chain(queryset1, queryset2)
    #
    # for obj in temp_queryset:
    #     try:
    #         qs1_object = queryset1.get(id=obj.id)
    #         qs2_object = queryset2.get(id=obj.id)
    #         if qs2_object.rank < qs1_object.rank:
    #             queryset2 = queryset2.exclude(id=obj.id)
    #         else:
    #             queryset1 = queryset1.exclude(id=obj.id)
    #     except ConsultantProfile.DoesNotExist:
    #         pass
    #
    # # queryset = queryset2 | queryset1
    # queryset = queryset1.union(queryset2)
    # # queryset = itertools.chain(queryset1, queryset2)
    # # result_queryset2 = queryset.none()
    # # for obj in queryset:
    # #     try:
    # #         qs1_object = queryset1.get(id=obj.id)
    # #         result_queryset2 |= queryset1.filter(id=obj.id)
    # #     except ConsultantProfile.DoesNotExist:
    # #         pass
    # #
    # #     try:
    # #         qs2_object = queryset2.get(id=obj.id)
    # #         result_queryset2 |= queryset2.filter(id=obj.id)
    # #     except ConsultantProfile.DoesNotExist:
    # #         pass
    #
    # # queryset = queryset1.union(queryset2)
    # #
    # # queryset = queryset.order_by('-rank')
    # # result_queryset = temp_queryset.none()
    #
    # # result_queryset = queryset.order_by('-rank')
    # #
    # # print(queryset)
    # # for obj in queryset:
    # #     print(obj.rank)
    #
    # if len(queryset) == 0:
    #     result_queryset = queryset.none()
    # else:
    #     result_queryset = queryset.order_by('-rank')
    #
    # return result_queryset

    queryset = qs.filter(active=True).annotate(
        rank=SearchRank(
            vector,
            query,
            normalization=Value(1),
        )
    ).filter(rank__gte=0.05).order_by('-rank')

    return queryset
