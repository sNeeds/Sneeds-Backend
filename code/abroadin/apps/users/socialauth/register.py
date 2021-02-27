from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from abroadin.apps.users.customAuth.serializers import UserSerializer

User = get_user_model()


def _register_user(data):
    user = User.objects.create_user(**data)
    user.is_verified = True
    user.save()

    return user


def get_user_jwt_tokens(user):
    data = {}
    refresh = RefreshToken.for_user(user)

    data['refresh'] = str(refresh)
    data['access'] = str(refresh.access_token)

    return data


def login_register_social_user(email, provider, first_name, last_name):
    assert provider in User.AuthProviderTypeChoices.values

    filtered_user = User.objects.filter(email=email)
    user_exists = filtered_user.exists()

    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'auth_provider': provider
    }

    if user_exists:
        user = filtered_user[0]
    else:
        user = _register_user(data)

    user_serializer = UserSerializer(user)
    tokens = get_user_jwt_tokens(user)

    return {
        'user': user_serializer.data,
        'access': tokens['access'],
        'refresh': tokens['refresh']
    }
