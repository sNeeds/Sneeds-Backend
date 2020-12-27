from abroadin.base.api.generics import CListAPIView, CRetrieveAPIView

from .serializers import ApplyProfileSerializer
from .models import ApplyProfile


class ApplyProfileAPIView(CListAPIView):
    queryset = ApplyProfile.objects.all()
    serializer_class = ApplyProfileSerializer


class ApplyProfileDetailAPIView(CRetrieveAPIView):
    lookup_field = 'id'
    queryset = ApplyProfile.objects.all()
    serializer_class = ApplyProfileSerializer
