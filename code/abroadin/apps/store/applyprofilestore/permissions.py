from rest_framework.permissions import BasePermission

from .models import SoldApplyProfileGroup


class ApplyProfileGroupOwner(BasePermission):
    message = "User should be the creator."

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            obj.user = request.user
        return True


class SoldApplyProfileGroupOwner(BasePermission):
    message = "User should be the buyer."

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            obj.sold_to = request.user
        return True


class BoughtApplyProfile(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            return obj.id in SoldApplyProfileGroup.user_bought_apply_profiles(request.user).only('id').values_list('id', flat=True)
        return True
