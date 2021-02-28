from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from google.auth.exceptions import GoogleAuthError

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, login_rule, user_eligible_for_login
from rest_framework_simplejwt.settings import api_settings

from .register import login_register_social_user
from .google import Google

User = get_user_model()


class TokenObtainPairWithoutPasswordSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        try:
            self.user = User.objects.get(email=authenticate_kwargs[self.username_field])
        except User.DoesNotExist:
            self.user = None

        if not getattr(login_rule, user_eligible_for_login)(self.user):
            raise AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        data = {}
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        try:
            user_data = Google.validate(auth_token)
        except GoogleAuthError as e:
            raise ValidationError(e.__str__())

        # if user_data['aud'] != GOOGLE_CLIENT_ID:
        #     raise AuthenticationFailed('Wrong Google Client ID')

        email = user_data['email']
        first_name = user_data['given_name']
        last_name = user_data['family_name']
        provider = User.AuthProviderTypeChoices.GOOGLE

        user = login_register_social_user(
            provider=provider, email=email, first_name=first_name, last_name=last_name
        )
        return {'email' : user.email}

