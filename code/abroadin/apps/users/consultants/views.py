from django.http import Http404
from django.db.models import F

from rest_framework.response import Response

from abroadin.base.api import generics
from abroadin.apps.users.consultants.models import ConsultantProfile
from abroadin.apps.users.consultants.serializers import ConsultantProfileSerializer
from abroadin.base.api.viewsets import CAPIView
from .paginators import StandardResultsSetPagination
from abroadin.apps.search.search_functions import search_consultants
from abroadin.apps.search.filter_functions import filter_consultants


class ConsultantProfileDetail(CAPIView):
    def get_object(self, slug):
        try:
            return ConsultantProfile.objects.get(slug=slug)
        except ConsultantProfile.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        consultant_profile = self.get_object(slug)
        serializer = ConsultantProfileSerializer(
            consultant_profile,
            context={"request": request}
        )
        return Response(serializer.data)


class ConsultantProfileList(generics.CListAPIView):
    serializer_class = ConsultantProfileSerializer
    pagination_class = StandardResultsSetPagination
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # If I delete this same objects will appear when paginating!
        # This is Django bug.
        # TODO: Report this bug
        len(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        qs = ConsultantProfile.objects.filter(active=True).at_least_one_time_slot()

        university = self.request.query_params.getlist("university")
        country = self.request.query_params.getlist("country")
        major = self.request.query_params.getlist("major")

        search_phrase = self.request.query_params.get('search', None)

        qs = filter_consultants(qs, university, country, major)

        qs = search_consultants(qs, search_phrase)

        if self.request.query_params.get("ordering") is not None:
            if "-rate" in self.request.query_params.get("ordering"):
                qs = qs.order_by(F('rate').desc(nulls_last=True))
            elif "rate" in self.request.query_params.get("ordering"):
                qs = qs.order_by(F('rate').asc(nulls_first=True))

        return qs
