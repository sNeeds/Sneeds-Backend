from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from rest_framework import permissions
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from abroadin.apps.estimation.form.models import StudentDetailedInfo, StudentDetailedInfoBase, SDI_CT


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


class IsWantToApplyOwnerOrDetailedInfoWithoutUser(permissions.BasePermission):
    message = "Only owner can view or edit object."

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user and user.is_authenticated:
            return obj.student_detailed_info.studentdetailedinfo.user == user
        if not user.is_authenticated:
            return obj.student_detailed_info.studentdetailedinfo.user is None

        return False
    pass


class CompletedForm(permissions.BasePermission):

    def has_permission(self, request, view):
        assert hasattr(view, 'lookup_url_kwarg'), \
            _('Missing form id lookup_url_kwarg in view: {}'.format(str(view)))
        assert view.kwargs.get(view.lookup_url_kwarg, None) is not None, \
            _('Missing form id lookup_url_kwarg "{}" in view {} kwargs.'.format(view.lookup_url_kwarg, str(view)))

        form = get_form_obj(view.kwargs.get(view.lookup_url_kwarg, None))
        if form:
            form.check_is_completed(raise_exception=True)
        return True

    def has_object_permission(self, request, view, obj):
        assert hasattr(view, 'lookup_url_kwarg'), \
            _('Missing form id lookup_url_kwarg in view: {}'.format(str(view)))
        assert view.kwargs.get(view.lookup_url_kwarg, None) is not None, \
            _('Missing form id lookup_url_kwarg "{}" in view {} kwargs.'.format(view.lookup_url_kwarg, str(view)))

        form = obj or get_form_obj(view.kwargs.get(view.lookup_url_kwarg, None))
        if form:
            form.check_is_completed(raise_exception=True)
        return True


class IsFormOwner(permissions.BasePermission):
    message = "User should be the owner of form"

    def has_permission(self, request, view):
        assert hasattr(view, 'lookup_url_kwarg'), \
            _('Missing form id lookup_url_kwarg in view: {}'.format(str(view)))
        assert view.kwargs.get(view.lookup_url_kwarg, None) is not None, \
            _('Missing form id lookup_url_kwarg "{}" in view {} kwargs.'.format(view.lookup_url_kwarg, str(view)))

        user = request.user
        if user and user.is_authenticated:
            form = get_form_obj(view.kwargs.get(view.lookup_url_kwarg, None))
            if form:
                return form.user == user
        return True

    def has_object_permission(self, request, view, obj: StudentDetailedInfo):
        assert hasattr(view, 'lookup_url_kwarg'), \
            _('Missing form id lookup_url_kwarg in view: {}'.format(str(view)))
        assert view.kwargs.get(view.lookup_url_kwarg, None) is not None, \
            _('Missing form id lookup_url_kwarg "{}" in view {} kwargs.'.format(view.lookup_url_kwarg, str(view)))

        user = request.user
        if user and user.is_authenticated:
            if obj:
                return obj.user == user
        return True


def get_form_obj(form_id):
    if form_id is None:
        return None
    try:
        return StudentDetailedInfo.objects.get(id=form_id)
    except StudentDetailedInfo.DoesNotExist:
        return None


class SDIThirdModelsWithGFPermission(permissions.BasePermission):
    message = "Only owner can view or edit object."

    def has_object_permission(self, request, view, obj):
        user = request.user
        # sdib_content_type = ContentType.objects.get_for_model(StudentDetailedInfoBase)

        if obj.content_type in [SDI_CT]:
            if user and user.is_authenticated:
                return obj.content_object.user == user
            if not user.is_authenticated:
                return obj.content_object.user is None
            return False

        return False


class IsLanguageCertificateOwnerOrDetailedInfoWithoutUser(SDIThirdModelsWithGFPermission):
    pass


class IsPublicationOwnerOrDetailedInfoWithoutUser(SDIThirdModelsWithGFPermission):
    pass


class IsEducationOwnerOrDetailedInfoWithoutUser(SDIThirdModelsWithGFPermission):
    pass