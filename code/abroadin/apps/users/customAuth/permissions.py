from rest_framework import permissions


class NotLoggedInPermission(permissions.BasePermission):
    message = 'You are already authenticates, please log out.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True


class SameUserPermission(permissions.BasePermission):
    message = "This user is not the user that is trying to access."

    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False


class UserEmailIsVerified(permissions.BasePermission):
    message = "User email is not verified."

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.is_email_verified
        return True

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
