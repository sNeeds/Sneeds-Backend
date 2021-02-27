from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from abroadin.settings.secure.APIs import GOOGLE_CLIENT_ID

from .register import login_register_social_user
from .google import Google

User = get_user_model()


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)

        try:
            user_data['sub']
        except Exception as e:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        # if user_data['aud'] != GOOGLE_CLIENT_ID:
        #     raise AuthenticationFailed('Wrong Google Client ID')

        print(user_data)
        email = user_data['email']
        name = user_data['name']
        first_name = user_data['given_name']
        last_name = user_data['family_name']
        provider = User.AuthProviderTypeChoices.GOOGLE

        print("**", provider)
        return login_register_social_user(
            provider=provider, email=email, name=name, first_name = first_name,
            last_name = last_name
        )
