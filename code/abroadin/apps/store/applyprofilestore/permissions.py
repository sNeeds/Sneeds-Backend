from rest_framework.permissions import BasePermission

from .models import SoldApplyProfileGroup


class ApplyProfileGroupOwner(BasePermission):
    message = "User should be the apply profile group owner."

    def has_object_permission(self, request, view, obj):
        return (not request.user.is_authenticated) or (request.user.is_authenticated and obj.user == request.user)


class SoldApplyProfileGroupOwner(BasePermission):
    message = "User should be the sold apply profile group buyer."

    def has_object_permission(self, request, view, obj):
        return (not request.user.is_authenticated) or (request.user.is_authenticated and obj.sold_to == request.user)


class BoughtApplyProfile(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            return obj.id in SoldApplyProfileGroup.user_bought_apply_profiles(request.user).only('id').values_list('id', flat=True)
        return True
