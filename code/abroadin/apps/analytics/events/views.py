import posthog
from rest_framework import status
from rest_framework.response import Response

from abroadin.base.api.viewsets import CAPIView
from apps.analytics.events.serializers import EventSerializer


class EventsList(CAPIView):
    def get_user_email_or_anonymous_string(self, user):
        if user.is_authenticated:
            return user.email
        return "Anonymous"

    def post(self, request, format=None):
        user_email = self.get_user_email_or_anonymous_string(request.user)
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            posthog.capture(user_email, event='test-event')
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
