from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from abroadin.base.api.generics import CListAPIView, CRetrieveAPIView

from .serializers import ApplyProfileSerializer
from .models import ApplyProfile
from ..estimation.form.models import StudentDetailedInfo
from ..estimation.similarprofiles.taggers import SimilarProfilesTagger


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

    def get_object(self):
        obj = super().get_object()

        # qs = self.get_queryset().filter(pk=obj.pk)
        comparison_sdi = self.request.query_params.get('comparison_student_detailed_info', None)
        if comparison_sdi:
            # obj.similar_gpa = True
            try:
                sdi = StudentDetailedInfo.objects.get(pk=comparison_sdi)
            except StudentDetailedInfo.DoesNotExist:
                raise NotFound
            return SimilarProfilesTagger.tag_object(obj, sdi)
        return obj
