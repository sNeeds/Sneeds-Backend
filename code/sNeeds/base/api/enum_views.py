from rest_framework.response import Response

from .viewsets import CAPIView


class EnumViewList(CAPIView):
    enum_class = None

    def get(self, request, *args, **kwargs):
        choices = self.enum_class.choices
        data = {
            "choices": [l for _, l in choices]
        }

        return Response(data)
