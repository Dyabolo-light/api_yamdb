from rest_framework import permissions


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.role == 'user' and request.user.is_authenticated
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.role == 'moderator' and request.user.is_authenticated
        )


class IsAdministator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.role == 'admin' and request.user.is_authenticated
        )


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.role == 'super_user' and request.user.is_authenticated
        )


class IsAnAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user in obj.authors:
            return True
        return False
