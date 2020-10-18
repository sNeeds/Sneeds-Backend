from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission
from sNeeds.apps.estimation.form.models import StudentDetailedInfo


class IsFormOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        sdi_id = view.kwargs.get('student_form', None)

        if sdi_id and user and user.is_authenticated:
            try:
                return StudentDetailedInfo.objects.get(id=sdi_id).user == user
            except StudentDetailedInfo.DoesNotExist:
                return False
        return False
