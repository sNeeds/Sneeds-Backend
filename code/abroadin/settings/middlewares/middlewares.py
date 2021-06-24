import pytz
from channels.auth import AuthMiddleware
from channels.auth import get_user as async_get_user
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.sessions import CookieMiddleware, SessionMiddleware

from django.utils import timezone
from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.headers.get("Client-Timezone")

        try:
            if tzname:
                timezone.activate(pytz.timezone(tzname))
            else:
                timezone.deactivate()
        except pytz.UnknownTimeZoneError:
            timezone.deactivate()

        return self.get_response(request)


class CORSMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = '*'
        response["Access-Control-Allow-Headers"] = 'Client-Timezone, authorization, content-type'
        response["Access-Control-Allow-Credentials"] = 'true'
        response["Access-Control-Allow-Methods"] = 'GET, PUT, POST, PATCH, DELETE, HEAD'

        return response


class UserActionsMiddleWare(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        response = self.get_response(request)

        try:
            if user.is_authenticated:
                user.update_date_last_action()
        except AuthenticationFailed: # Errors are not caught in middleware
            pass
        return response


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)

        if user.is_authenticated:
            return user

        if authentication.JWTAuthentication().authenticate(request):
            user = authentication.JWTAuthentication().authenticate(request)[0]

        return user


@database_sync_to_async
async def get_jwt_user(scope):

    print('injaaaaaa1')
    user = await async_get_user(scope)

    print('2', user)

    print('2.5', user.is_authenticated)

    if user.is_authenticated:
        return user

    authenticated_users_by_jwt = authentication.JWTAuthentication().authenticate(scope['request'])

    print('3', authenticated_users_by_jwt)
    if authenticated_users_by_jwt:
        user = authenticated_users_by_jwt[0]

    return user


class ChannelsJWTAuthenticationMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        """
        ASGI application; can insert things into the scope and run asynchronous
        code.
        """
        # Copy scope to stop changes going upstream
        scope = dict(scope)
        scope['user'] = await get_jwt_user(scope)

        print('mmmm', self.inner)

        return await self.inner(scope, receive, send)


def AuthMiddlewareStack(inner):
    # return CookieMiddleware(SessionMiddleware(AuthMiddleware(ChannelsJWTAuthenticationMiddleware(inner))))
    return CookieMiddleware(SessionMiddleware(AuthMiddleware(inner)))