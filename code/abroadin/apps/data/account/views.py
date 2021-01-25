from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import F
from django.db.models.functions import Length, Ln

from abroadin.base.api import generics

from . import models
from . import serializers
from ...search.search_functions import search_country, search_university, search_major


class CountryDetail(generics.CRetrieveAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    lookup_field = 'slug'


class CountryList(generics.CListAPIView):
    serializer_class = serializers.CountrySerializer

    def get_queryset(self):
        request = self.request
        with_time_slot_consultants = request.query_params.get('with-time-slot-consultants', None)
        search_terms = request.query_params.get('search', '')

        if with_time_slot_consultants == 'true':
            qs = models.Country.objects.with_active_time_slot_consultants().exclude(slug="iran")
        else:
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
        from abroadin.apps.users.consultants.models import StudyInfo
        study_info_with_active_consultant_qs = StudyInfo.objects.all().with_active_consultants()
        university_list = list(study_info_with_active_consultant_qs.values_list('university_id', flat=True))
        return models.University.objects.filter(id__in=university_list)


class UniversityForFormList(generics.CListAPIView):
    queryset = models.University.objects.none()
    serializer_class = serializers.UniversitySerializer

    def get_queryset(self):
        request = self.request
        search_terms = request.query_params.get('search', '')
        search_term = search_terms[:16]
        search_result = search_university(models.University.objects.all(), search_term)

        return search_result


class MajorDetail(generics.CRetrieveAPIView):
    queryset = models.Major.objects.all()
    serializer_class = serializers.MajorSerializer
    lookup_field = 'id'


class MajorList(generics.CListAPIView):
    serializer_class = serializers.MajorSerializer

    def get_queryset(self):
        from abroadin.apps.users.consultants.models import StudyInfo
        study_info_with_active_consultant_qs = StudyInfo.objects.all().with_active_consultants()
        major_list = list(study_info_with_active_consultant_qs.values_list('major__id', flat=True))
        return models.Major.objects.filter(id__in=major_list)


class MajorForFormList(generics.CListAPIView):
    queryset = models.Major.objects.none()
    serializer_class = serializers.MajorSerializer

    def get_queryset(self):
        request = self.request
        search_terms = request.query_params.get('search', '')
        search_term = search_terms[:16]
        search_result = search_major(models.Major.objects.all(), search_term)

        return search_result
