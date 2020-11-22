from django.contrib.auth import get_user_model

from rest_framework import permissions, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from verification.views import BaseGenerateVerificationAPIView, BaseVerifyVerificationAPIView

from abroadin.base.api.viewsets import CAPIView
from abroadin.base.api import generics

from . import serializers
from .serializers import (UserRegisterSerializer,
                          SubscribeSerializer)
from .permissions import (NotLoggedInPermission,
                          SameUserPermission)
from .utils import send_verification_code, check_email_assigned_to_user, set_user_receive_marketing_email

User = get_user_model()


class UserListView(generics.CCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [NotLoggedInPermission]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated'}, status=400)
        return self.create(request, *args, **kwargs)


class UserDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.CGenericAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, SameUserPermission]

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs.get('id', None):
            return Response({"detail": "You are not logged in as this user."}, 403)
        return self.retrieve(request)

    def put(self, request, *args, **kwargs):
        if request.user.id != kwargs.get('id', None):
            return Response({"detail": "You are not logged in as this user."}, 403)
        return self.update(request)


class MyAccountInfoView(CAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request):
        my_account = self.get_object()
        serializer = serializers.MyAccountSerializer(my_account, context={"request": request})
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


class GenerateVerificationAPIView(BaseGenerateVerificationAPIView):
    send_code_function = send_verification_code


class VerifyVerificationAPIView(BaseVerifyVerificationAPIView):
    post_check_function = None


class SubscribeAPIView(generics.CCreateAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if check_email_assigned_to_user(serializer.validated_data['email']):
            set_user_receive_marketing_email(serializer.validated_data['email'])
            print(1)
        else:
            self.perform_create(serializer)
            print(2)
        data = serializer.validated_data
        data['phone_number'] = str(data['phone_number'])
        return Response(data, status=status.HTTP_201_CREATED)
