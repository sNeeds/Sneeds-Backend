from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import F
from django.db.models.functions import Length, Ln

from abroadin.base.api import generics

from . import models
from . import serializers
from ...search.search_functions import search_country, limited_query_search_major, limited_query_search_university


class CountryDetail(generics.CRetrieveAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    lookup_field = 'slug'


class CountryList(generics.CListAPIView):
    serializer_class = serializers.CountrySerializer

    def get_queryset(self):
        request = self.request
        search_terms = request.query_params.get('search', '')
        qs = models.Country.objects.all()

        search_term = search_terms[:16]
        search_result = search_country(qs, search_term)

        return search_result


class UniversityDetail(generics.CRetrieveAPIView):
    queryset = models.University.objects.all()
    serializer_class = serializers.UniversitySerializer
    lookup_field = 'id'


class UniversityList(generics.CListAPIView):
    serializer_class = serializers.UniversitySerializer

    def get_queryset(self):
        return models.University.objects.all()


class UniversityForFormList(generics.CListAPIView):
    queryset = models.University.objects.none()
    serializer_class = serializers.UniversitySerializer

    def get_queryset(self):
        request = self.request
        search_terms = request.query_params.get('search', '')
        search_result = limited_query_search_university(models.University.objects.all(), search_terms)

        return search_result


class MajorDetail(generics.CRetrieveAPIView):
    queryset = models.Major.objects.all()
    serializer_class = serializers.MajorSerializer
    lookup_field = 'id'


class MajorList(generics.CListAPIView):
    serializer_class = serializers.MajorSerializer

    def get_queryset(self):
        return models.Major.objects.all()


class MajorForFormList(generics.CListAPIView):
    queryset = models.Major.objects.none()
    serializer_class = serializers.MajorSerializer

    def get_queryset(self):
        request = self.request
        search_terms = request.query_params.get('search', '')
        search_term = search_terms[:16]
        search_result = limited_query_search_major(models.Major.objects.all(), search_term)

        return search_result
