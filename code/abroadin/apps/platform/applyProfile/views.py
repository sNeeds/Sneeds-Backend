from abroadin.base.api.generics import CListAPIView

from .serializers import ApplyProfileSerializer
from .models import ApplyProfile


class ApplyProfileAPIView(CListAPIView):
    queryset = ApplyProfile.objects.all()
    serializer_class = ApplyProfileSerializer
