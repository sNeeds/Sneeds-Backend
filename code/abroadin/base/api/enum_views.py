from rest_framework.response import Response

from .viewsets import CAPIView


class EnumViewList(CAPIView):
    enum_class = None
    include = []
    exclude = []

    def get(self, request, *args, **kwargs):
        assert (not self.include and not self.exclude) or (self.include and not self.exclude) or (not self.include and self.exclude),\
            "Both include and exclude can not have values."

        # if self.include:
        #     assert not self.enum_class, "enum_class is redundant when include list has value."

        assert (not self.include) or (self.include and not self.enum_class),\
            "enum_class is redundant when include list has value."

        assert (not self.exclude) or (self.exclude and self.enum_class),\
            "exclude list has value but enum_class is not set."

        if self.include:
            data = [enum.value for enum in self.include]
        else:
            choices = self.enum_class.choices
            data = [value for name, value in choices if name not in self.exclude]
        return Response(data)
