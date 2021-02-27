import os

from django.contrib.auth import authenticate, get_user_model

from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


def _authenticate_user(user):
    user = authenticate(
        email=user.email,
        password=os.environ.get('SOCIAL_SECRET')
    )
    return user


def _register_user(data):
    user = User.objects.create_user(**data)
    user.is_verified = True
    user.save()
    return user


def _handle_existed_user(user, auth_provider):

    if auth_provider == user.auth_provider:
        authenticated_user = _authenticate_user(user)
    else:
        raise AuthenticationFailed(
            detail='User is registered, Please continue your \
            login using ' + user.auth_provider
        )
    return authenticated_user


def _handle_new_user(data):
    user = _register_user(data)
    authenticated_user = _authenticate_user(user)
    return authenticated_user


def register_social_user(email, provider, first_name, last_name ):
    assert provider in User.AuthProviderTypeChoices.values

    filtered_user = User.objects.filter(email=email)
    user_exists = filtered_user.exists()

    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'aut_provider': provider
    }

    if user_exists:
        user = filtered_user[0]
        user = _handle_existed_user(user, data['email'])
    else:
        user = _handle_new_user(data)

    return {
        'email': user.email,
        'tokens': user.tokens()
    }
