from django.db import models
from django.utils import six
from functools import reduce
from rest_framework.compat import (
    coreapi, coreschema, distinct, is_guardian_installed
)
import operator

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.contrib.postgres.search import SearchQuery, SearchRank

from sNeeds.apps.account.models import BasicFormField


class BasicFormFieldSearch(SearchFilter):


    def filter_queryset(self, request, queryset, view):

        print("HOY HOY HOY")
        params = request.query_params.get('search', '')
        search_terms = params.replace(',', ' ').split()

        if not search_terms:
            return queryset

        if len(search_terms) == 0:
            return queryset

        search_term = search_terms[0]

        print(search_term)

        search_term = search_term[:32]
        search_query = SearchQuery(search_term, search_type='plain')

        base = queryset
        queryset = base.annotate(rank=SearchRank('name_search', search_query)).order_by('-rank')
        return queryset
