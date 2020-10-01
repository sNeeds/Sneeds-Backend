from rest_framework.filters import SearchFilter
from django.contrib.postgres.search import SearchQuery, SearchRank


class BasicFormFieldSearch(SearchFilter):


    def filter_queryset(self, request, queryset, view):

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
