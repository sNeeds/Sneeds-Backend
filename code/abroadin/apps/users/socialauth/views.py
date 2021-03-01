from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from abroadin.base.api.generics import CGenericAPIView

from .serializers import GoogleSocialAuthSerializer, TokenObtainPairWithoutPasswordSerializer, \
    FacebookSocialAuthSerializer


class SocialAuthView(CGenericAPIView):
    token_serializer_class = TokenObtainPairWithoutPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = (serializer.validated_data)['user']

        data = {'email': user.email}
        token_serializer = self.token_serializer_class(data=data)

        try:
            token_serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(token_serializer.validated_data, status=status.HTTP_200_OK)


class GoogleSocialAuthView(SocialAuthView):
    serializer_class = GoogleSocialAuthSerializer


class FacebookSocialAuthView(SocialAuthView):
    serializer_class = FacebookSocialAuthSerializer
