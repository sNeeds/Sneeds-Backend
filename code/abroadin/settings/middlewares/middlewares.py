import pytz

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
        response["Access-Control-Allow-Origin"] = "*"
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
