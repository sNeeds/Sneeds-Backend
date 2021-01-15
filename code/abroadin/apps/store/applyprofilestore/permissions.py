from rest_framework.permissions import BasePermission

from .models import SoldApplyProfileGroup

class BoughtApplyProfile(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return SoldApplyProfileGroup.objects.filter(apply_profiles=)