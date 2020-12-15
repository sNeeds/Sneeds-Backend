from django.utils.translation import gettext_lazy as _

from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

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


class CompletedForm(permissions.BasePermission):
    completed_credential = {
        "_has_age":
            {'section': 'personal', 'model': 'StudentDetailedInfo', 'fields': ['age'], 'detail': ''},
        "_has_is_married":
            {'section': 'personal', 'model': 'StudentDetailedInfo', 'fields': ['is_married'], 'detail': ''},
        "_has_gender":
            {'section': 'personal', 'model': 'StudentDetailedInfo', 'fields': ['gender'], 'detail': ''},
        "_has_university_through":
            {'section': 'academic_degree', 'model': 'UniversityThrough', 'fields': ['age'], 'detail': ''},
        "_has_want_to_apply":
            {'section': 'apply_destination', 'model': 'WantToApply', 'fields': [], 'detail': ''},
    }

    assert completed_credential.keys() == StudentDetailedInfo.completed_funcs, (
        _("Inconsistency in form completeness check functions")
    )

    def has_permission(self, request, view):
        form = get_form_obj(view.kwargs.get(view.lookup_url_kwarg, None))
        errors = []
        if form is None:
            return False
        completed = True
        for func_str in self.completed_credential:
            if not getattr(form, func_str)():
                errors.append(self.completed_credential[func_str])
                completed = False
        if not completed:
            raise ValidationError({
                    api_settings.NON_FIELD_ERRORS_KEY: errors
                })
        return True

    def has_object_permission(self, request, view, obj):
        errors = []
        if obj is None:
            return False
        completed = True
        for func_str in self.completed_credential:
            if not getattr(obj, func_str)():
                errors.append(self.completed_credential[func_str])
                completed = False
        if not completed:
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: errors
            })
        return True


def get_form_obj(form_id):
    if form_id is None:
        return None
    try:
        return StudentDetailedInfo.objects.get(id=form_id)
    except StudentDetailedInfo.DoesNotExist:
        return None
