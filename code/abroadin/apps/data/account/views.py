from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import F
from django.db.models.functions import Length, Ln

from abroadin.base.api import generics

from . import models
from . import serializers


class CountryDetail(generics.CRetrieveAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    lookup_field = 'slug'


class CountryList(generics.CListAPIView):
    serializer_class = serializers.CountrySerializer

    def get_queryset(self):
        request = self.request
        with_time_slot_consultants = request.query_params.get('with-time-slot-consultants', None)
        search_terms = request.query_params.get('search', None)

        qs = models.Country.objects.all()
        other_qs = models.Country.objects. \
            annotate(similarity=TrigramSimilarity('search_name', 'سایر'),
                     search_name_length=Ln(Length('search_name'))). \
            annotate(t=F('similarity') * F('search_name_length')). \
            filter(t__gt=0.4).order_by('-t')

        if with_time_slot_consultants == 'true':
            qs = models.Country.objects.with_active_time_slot_consultants().exclude(slug="iran")

        if search_terms is not None:
            search_term = search_terms[:16]
            if len(search_term) == 0:
                return other_qs

            # To see execution time of queries, use this: python manage.py shell_plus --print-sql
            # To see results use endpoint /form-universities?&search=colombia
            qs = qs.annotate(similarity=TrigramSimilarity('search_name', search_term),
                             search_name_length=Ln(Length('search_name'))). \
                annotate(t=F('similarity') * F('search_name_length')). \
                filter(t__gt=0.4).order_by('-t')

            qs |= other_qs

        qs = qs.distinct()
        return qs


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
        params = request.query_params.get('search', '')
        search_terms = params

        other_qs = models.University.objects. \
            annotate(similarity=TrigramSimilarity('search_name', 'سایر'),
                     search_name_length=Ln(Length('search_name'))). \
            annotate(t=F('similarity') * F('search_name_length')). \
            filter(t__gt=0.4).order_by('-t')

        if not search_terms:
            return other_qs

        search_term = search_terms[:16]
        if len(search_term) < 4:
            return other_qs

        # To see execution time of queries, use this: python manage.py shell_plus --print-sql
        # To see results use endpoint /form-universities?&search=colombia
        qs = models.University.objects. \
            annotate(similarity=TrigramSimilarity('search_name', search_term),
                     search_name_length=Ln(Length('search_name'))). \
            annotate(t=F('similarity') * F('search_name_length')). \
            filter(t__gt=0.4).order_by('-t')

        qs = qs | other_qs
        qs = qs.distinct()

        return qs


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
        params = request.query_params.get('search', '')
        search_terms = params

        other_qs = models.Major.objects. \
            annotate(similarity=TrigramSimilarity('search_name', 'سایر'),
                     search_name_length=Ln(Length('search_name'))). \
            annotate(t=F('similarity') * F('search_name_length')). \
            filter(t__gt=0.4).order_by('-t')

        if not search_terms:
            return other_qs

        search_term = search_terms[:16]
        if len(search_term) < 4:
            return other_qs

        # To see execution time of queries, use this: python manage.py shell_plus --print-sql
        # To see results use endpoint /form-universities?&search=colombia
        qs = models.Major.objects. \
            annotate(similarity=TrigramSimilarity('search_name', search_term),
                     search_name_length=Ln(Length('search_name'))). \
            annotate(t=F('similarity') * F('search_name_length')). \
            filter(t__gt=0.4).order_by('-t')

        qs = qs | other_qs
        qs = qs.distinct()

        return qs
