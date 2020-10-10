from rest_framework import views

from .viewmixins import CAPIViewPatch200Mixin


class CAPIView(CAPIViewPatch200Mixin, views.APIView):
    pass
