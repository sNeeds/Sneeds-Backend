import pytz

from django.utils import timezone


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

        if user:
            user.update_date_last_action()
        return response
