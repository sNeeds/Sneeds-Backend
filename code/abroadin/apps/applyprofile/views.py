from rest_framework.pagination import PageNumberPagination

from abroadin.base.api.generics import CListAPIView, CRetrieveAPIView

from .serializers import ApplyProfileSerializer
from .models import ApplyProfile


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


class ApplyProfileAPIView(CListAPIView):
    queryset = ApplyProfile.objects.all()
    serializer_class = ApplyProfileSerializer
    pagination_class = SmallResultsSetPagination


class ApplyProfileDetailAPIView(CRetrieveAPIView):
    lookup_field = 'id'
    queryset = ApplyProfile.objects.all()
    serializer_class = ApplyProfileSerializer

