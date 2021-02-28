from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from abroadin.base.api.generics import CGenericAPIView

from .serializers import GoogleSocialAuthSerializer, TokenObtainPairWithoutPasswordSerializer
from ..customAuth.serializers import CustomTokenObtainPairSerializer


class GoogleSocialAuthView(CGenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)['auth_token']

        print("->>", data)

        data = {
            'email': "bartararya@gmail.com"
        }

        token_serializer = TokenObtainPairWithoutPasswordSerializer(
            data=data
        )

        try:
            token_serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(token_serializer.validated_data, status=status.HTTP_200_OK)
