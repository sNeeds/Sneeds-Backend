from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Value

from sNeeds.apps.users.consultants.models import ConsultantProfile, StudyInfo


def search_consultants(qs, phrase):
    vector = SearchVector('user__first_name', weight='B') + SearchVector('user__last_name', weight='B') +\
             SearchVector('bio', weight='A')
    query = SearchQuery(phrase, search_type='websearch')
    ids1 = set(StudyInfo.objects.filter(university__country__search_name__search=phrase).values_list('consultant__id',
                                                                                                     flat=True))
    ids2 = set(StudyInfo.objects.filter(university__search_name__search=phrase).values_list('consultant__id',
                                                                                            flat=True))
    ids3 = set(StudyInfo.objects.filter(major__search_name__search=phrase).values_list('consultant__id',
                                                                                       flat=True))

    ids = ids1 | ids2 | ids3

    queryset1 = ConsultantProfile.objects.filter(id__in=ids, active=True)
    queryset2 = qs.filter(active=True).annotate(
        rank=SearchRank(
            vector,
            query,
            normalization=Value(2).bitor(Value(4)),
        )
    ).filter(rank__gte=0.3).order_by('rank')

    queryset = queryset1 | queryset2

    return queryset
