from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Value, FloatField

from sNeeds.apps.users.consultants.models import ConsultantProfile, StudyInfo


def search_consultants(qs, phrase):
    if phrase is None:
        return qs

    vector = SearchVector('user__first_name', weight='B') + SearchVector('user__last_name', weight='B') + \
             SearchVector('bio', weight='A')

    query = SearchQuery(phrase, search_type='websearch')
    ids1 = set(StudyInfo.objects.filter(university__country__search_name__search=phrase).values_list('consultant__id',
                                                                                                     flat=True))
    ids2 = set(StudyInfo.objects.filter(university__search_name__search=phrase).values_list('consultant__id',
                                                                                            flat=True))
    ids3 = set(StudyInfo.objects.filter(major__search_name__search=phrase).values_list('consultant__id',
                                                                                       flat=True))

    ids = ids1 | ids2 | ids3

    # https://stackoverflow.com/questions/3590306/django-static-annotation
    queryset1 = ConsultantProfile.objects.filter(id__in=ids, active=True).annotate(rank=Value(10, FloatField()))

    queryset2 = qs.filter(active=True).annotate(
        rank=SearchRank(
            vector,
            query,
            normalization=Value(2).bitor(Value(4)),
        )
    )

    temp_queryset = queryset1 | queryset2

    for obj in temp_queryset:
        try:
            qs1_object = queryset1.get(id=obj.id)
            qs2_object = queryset2.get(id=obj.id)
            if qs1_object.rank > qs2_object.rank:
                queryset2 = queryset2.exclude(id=obj.id)
            else:
                queryset1 = queryset1.exclude(id=obj.id)
        except ConsultantProfile.DoesNotExist:
            pass

    queryset = queryset1.union(queryset2)

    queryset = queryset.order_by('-rank')

    return queryset
