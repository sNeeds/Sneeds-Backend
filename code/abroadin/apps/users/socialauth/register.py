from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def _register_user(*args, **kwargs):
    user = User.objects.create_user(**kwargs)
    user.is_verified = True
    user.is_email_verified = True
    user.set_unusable_password()
    user.save()
    print('**->> user registered, Password is: ' , user.password)
    return user


def get_jwt_tokens(user):
    data = {}
    refresh = RefreshToken.for_user(user)

    data['refresh'] = str(refresh)
    data['access'] = str(refresh.access_token)

    return data


def login_register_social_user(email, provider, first_name, last_name):
    assert provider in User.AuthProviderTypeChoices.values

    filtered_user = User.objects.filter(email=email)
    user_exists = filtered_user.exists()

    if user_exists:
        user = filtered_user[0]
        user.auth_provider = provider
        user.save()
    else:
        user = _register_user(
            email=email, first_name=first_name, last_name=last_name,
            auth_provider=provider
        )

    return user