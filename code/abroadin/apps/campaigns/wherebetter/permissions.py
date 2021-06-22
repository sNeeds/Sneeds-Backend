from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class IsParticipantOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsInviteInfoOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.invitor_user == request.user


class URLUserMatchReqUser(BasePermission):

    def has_permission(self, request, view):
        assert hasattr(view, 'lookup_url_kwarg'), \
            _('Missing user id lookup_url_kwarg in view: {}'.format(str(view)))
        user_id = view.kwargs.get(view.lookup_url_kwarg, None)
        if user_id:
            return user_id == request.user.id
        return True
