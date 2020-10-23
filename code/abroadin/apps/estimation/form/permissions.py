from rest_framework import permissions

from abroadin.apps.estimation.form.models import StudentDetailedInfo


class OnlyOneFormPermission(permissions.BasePermission):
    message = "Student can only have one form."

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return not StudentDetailedInfo.objects.filter(user=request.user).exists()
        return True


class SameUserOrNone(permissions.BasePermission):
    message = "Form owner is set and only owner can see/update this form."

    def has_object_permission(self, request, view, obj):
        if obj.user is None:
            return True

        user = request.user
        if user.is_authenticated:
            return obj.user == user

        return False



class UserAlreadyHasForm(permissions.BasePermission):
    message = "User has an active form and cannot update this form to it's own."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            try:
                return StudentDetailedInfo.objects.get(user__id=user.id).id == obj.id
            except StudentDetailedInfo.DoesNotExist:
                pass

        return True


class SDIThirdModelsPermission(permissions.BasePermission):
    message = "Only owner can view or edit object."

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user and user.is_authenticated:
            return obj.student_detailed_info.studentdetailedinfo.user == user
        if not user.is_authenticated:
            return obj.student_detailed_info.studentdetailedinfo.user is None

        return False


class IsLanguageCertificateOwnerOrDetailedInfoWithoutUser(SDIThirdModelsPermission):
    pass


class IsPublicationOwnerOrDetailedInfoWithoutUser(SDIThirdModelsPermission):
    pass


class IsWantToApplyOwnerOrDetailedInfoWithoutUser(SDIThirdModelsPermission):
    pass


class IsUniversityThroughOwnerOrDetailedInfoWithoutUser(SDIThirdModelsPermission):
    pass
