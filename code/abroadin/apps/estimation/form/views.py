from drf_yasg.utils import swagger_auto_schema

from abroadin.base.api import generics
from abroadin.base.api.permissions import permission_class_factory

from .models import StudentDetailedInfo

from .serializers import StudentDetailedInfoSerializer, StudentDetailedInfoRequestSerializer
from .permissions import OnlyOneFormPermission, SameUserOrNone, UserAlreadyHasForm


class StudentDetailedInfoListCreateView(generics.CListCreateAPIView):
    queryset = StudentDetailedInfo.objects.all()
    serializer_class = StudentDetailedInfoSerializer
    request_serializer_class = StudentDetailedInfoSerializer
    permission_classes = [
        permission_class_factory(OnlyOneFormPermission, ["POST"])
    ]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return StudentDetailedInfo.objects.none()
        qs = StudentDetailedInfo.objects.filter(user=user)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            super().perform_create(serializer)

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StudentDetailedInfoRetrieveUpdateView(generics.CRetrieveAPIView):
    lookup_field = 'id'
    queryset = StudentDetailedInfo.objects.all()
    serializer_class = StudentDetailedInfoSerializer
    request_serializer_class = StudentDetailedInfoRequestSerializer

    permission_classes = [
        permission_class_factory(SameUserOrNone, ["GET", "PUT", "PATCH"]),
        permission_class_factory(UserAlreadyHasForm, ["PUT", "PATCH"])
    ]

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            super().perform_update(serializer)

    def partial_update(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            request.data.update({"user": user.id})
        return super().partial_update(request, *args, **kwargs)

