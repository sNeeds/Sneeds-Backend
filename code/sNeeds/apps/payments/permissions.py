from rest_framework.permissions import BasePermission
from sNeeds.apps.consultants.models import ConsultantProfile


class ConsultantDepositInfoOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "OPTIONS":
            return True

        if obj.consultant.user == request.user:
            return True

        return False
