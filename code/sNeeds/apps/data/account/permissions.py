from rest_framework import permissions

from sNeeds.apps.store.storePackages.models import SoldStorePackage


class IsStudentPermission(permissions.BasePermission):
    message = "Only student users can create StudentDetailedInfo"

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        else:
            return user.is_student()


class StudentDetailedInfoOwnerOrInteractConsultantOrWithoutUserPermission(permissions.BasePermission):
    message = "Only owner can update and only owner and consultants that service the owner can see info"

    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.user is None:
            return True

        user = request.user
        if user:
            if obj.user == user:
                return True
            elif request.method == 'GET' and user.is_authenticated and user.is_consultant():
                """when user has bought a package, every consultant can see the form
                and if had not bought package any other user can not see that. in this situation to let consultants that
                had time slot with user to see the form uncommnet the qs_2 line"""
                # qs_1 = get_consultants_interact_with_user(user=obj.user).filter(user=user)

                # TODO If all sold store packages of user have consultant, other consultants won't access the form
                qs_2 = SoldStorePackage.objects.filter(sold_to=obj.user)
                return qs_2.exists()


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
