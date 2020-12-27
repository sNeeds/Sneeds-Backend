from abroadin.base.api.generics import CListAPIView, CRetrieveAPIView

from .serializers import ApplyProfileSerializer, AdmissionSerializer
from .models import ApplyProfile, Admission


class ApplyProfileAPIView(CListAPIView):
    queryset = ApplyProfile.objects.all()
    serializer_class = ApplyProfileSerializer


class ApplyProfileDetailAPIView(CRetrieveAPIView):
    lookup_field = 'id'
    queryset = ApplyProfile.objects.all()
    serializer_class = ApplyProfileSerializer


class AdmissionListAPIView(CListAPIView):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer


class AdmissionDetailAPIView(CRetrieveAPIView):
    lookup_field = 'id'
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer


