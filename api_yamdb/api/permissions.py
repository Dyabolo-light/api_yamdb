from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.role == 'admin'
                         or request.user.is_superuser
                         or request.user.is_staff)))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.role == 'admin'
                         or request.user.is_superuser
                         or request.user.is_staff)))


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.role == 'user' and request.user.is_authenticated
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.role == 'moderator' and request.user.is_authenticated)


class IsAdministator(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.user.role == 'admin' or request.user.is_superuser)
                and request.user.is_authenticated)


class IsAnAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user in obj.authors:
            return True
        return False


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return (
            user.is_authenticated and (
                obj.author == user or user.role == 'moderator' or user.role == 'admin'
            )
        )