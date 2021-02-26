from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from abroadin.settings.secure.APIs import GOOGLE_CLIENT_ID

from .register import register_social_user
from .google import Google


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

        if user_data['aud'] != GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('Wrong Google Client ID')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)
