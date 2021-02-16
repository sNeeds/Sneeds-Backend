import itertools

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Value, FloatField, F
from django.db.models.functions import Ln, Length

from abroadin.apps.data.account.models import Country
from abroadin.apps.users.consultants.models import ConsultantProfile, StudyInfo

UNIVERSITY_MAX_QUERY_LENGTH = 10
MAJOR_MAX_QUERY_LENGTH = 10


def search_consultants(qs, phrase):
    if phrase is None:
        return qs

    vector = SearchVector('user__first_name', weight='B') + SearchVector('user__last_name', weight='B') \
             + SearchVector('bio', weight='B') \
             + SearchVector('studyinfo__university__country__search_name', weight='A') \
             + SearchVector('studyinfo__university__search_name', weight='A') \
             + SearchVector('studyinfo__major__search_name', weight='A')

    query = SearchQuery(phrase, search_type='websearch')

    queryset = qs.filter(active=True).annotate(
        rank=SearchRank(
            vector,
            query,
            normalization=Value(1),
        )
    ).filter(rank__gte=0.05).order_by('-rank')

    return queryset


def search_country(qs, phrase):
    # To see execution time of queries, use this: python manage.py shell_plus --print-sql
    # To see results use endpoint /form-universities?&search=colombia
    other_queryset = qs.filter(search_name__icontains='other').annotate(
        similarity=Value(0.001, output_field=FloatField()),
        search_name_length=Value(0.001, output_field=FloatField()),
        t=Value(0.001, output_field=FloatField()))

    if phrase is None or len(phrase) == 0:
        return qs

    queryset = qs.annotate(similarity=TrigramSimilarity('search_name', phrase),
                           search_name_length=Ln(Length('search_name'))). \
        annotate(t=F('similarity') * F('search_name_length')). \
        filter(t__gt=0.4).order_by('-t')

    return queryset | other_queryset


def search_university(qs, phrase: str):
    other_queryset = qs.filter(search_name__istartswith='other').annotate(
        similarity=Value(0.001, output_field=FloatField()),
        search_name_length=Value(0.001, output_field=FloatField()),
        t=Value(0.001, output_field=FloatField()))

    if phrase is None or len(phrase) == 0:
        return other_queryset

    queryset = qs.annotate(similarity=TrigramSimilarity('search_name', phrase),
                           search_name_length=Ln(Length('search_name'))). \
        annotate(t=F('similarity') * F('search_name_length')). \
        filter(t__gt=0.4).order_by('-t')

    return queryset | other_queryset


def shorten_university_query(phrase: str):
    phrase = phrase.lower()
    phrase = phrase.replace('university', '')
    phrase = phrase.replace('of', '')
    phrase = phrase.strip()
    if len(phrase) > UNIVERSITY_MAX_QUERY_LENGTH:
        pieces = phrase.split(' ')
        if len(pieces) == 1:
            phrase = phrase[:UNIVERSITY_MAX_QUERY_LENGTH]
        else:
            refined_pieces = []
            it_limit = 3 if len(pieces) > 3 else len(pieces)
            for i in range(0, it_limit):
                if len(pieces[i]) > 0: refined_pieces.append(pieces[i][:4])
            phrase = ' '.join(refined_pieces)

    return phrase


def limited_query_search_university(qs, phrase: str):
    phrase = shorten_university_query(phrase)
    return search_university(qs, phrase)


def search_major(qs, phrase):
    other_queryset = qs.filter(search_name__istartswith='other').annotate(
        similarity=Value(0.001, output_field=FloatField()),
        search_name_length=Value(0.001, output_field=FloatField()),
        t=Value(0.001, output_field=FloatField()))

    if phrase is None or len(phrase) == 0:
        return other_queryset

    queryset = qs.annotate(similarity=TrigramSimilarity('search_name', phrase),
                           search_name_length=Ln(Length('search_name'))). \
        annotate(t=F('similarity') * F('search_name_length')). \
        filter(t__gt=0.4).order_by('-t')

    return queryset | other_queryset


def shorten_major_query(phrase: str):
    phrase = phrase.lower()
    phrase = phrase.strip()

    if len(phrase) > MAJOR_MAX_QUERY_LENGTH:
        pieces = phrase.split(' ')
        if len(pieces) == 1:
            phrase = phrase[:MAJOR_MAX_QUERY_LENGTH]
        else:
            refined_pieces = []
            it_limit = 3 if len(pieces) > 3 else len(pieces)
            for i in range(0, it_limit):
                if len(pieces[i]) > 0: refined_pieces.append(pieces[i][:4])
            phrase = ' '.join(refined_pieces)

    return phrase


def limited_query_search_major(qs, phrase: str):
    phrase = shorten_major_query(phrase)
    return search_major(qs, phrase)
