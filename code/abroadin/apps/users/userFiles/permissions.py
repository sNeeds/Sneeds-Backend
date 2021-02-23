from rest_framework import permissions

from abroadin.apps.users.consultants.models import ConsultantProfile


class UserFileOwnerPermission(permissions.BasePermission):
    message = "This user is not file owner."

    def has_object_permission(self, request, view, obj):
        user = request.user
        consultant_profile_qs = ConsultantProfile.objects.filter(user=user)

        # Checks if user has bought a time slot from this consultant
        if request.method in permissions.SAFE_METHODS and consultant_profile_qs.exists():
            consultant_profile = consultant_profile_qs.first()

        if user == obj.user:
            return True

        return False
