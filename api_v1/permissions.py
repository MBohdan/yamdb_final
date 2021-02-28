from rest_framework.permissions import (SAFE_METHODS, BasePermission)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff


class ReviewCommentPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                and request.user.is_anonymous
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ("PATCH", "DELETE"):
            return (obj.author == request.user
                    or request.user.is_admin
                    or request.user.is_moderator
                    )
        return True


class IsAdmin(BasePermission):
    message = 'Не хватает прав, нужны права'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


# class IsSuperuser(BasePermission):
#     message = 'Не хватает прав, нужны права Администратора Django'
#
#     def has_permission(self, request, view):
#         return (request.user.is_authenticated
#                 and request.user.is_superuser)
#
#     def has_object_permission(self, request, view, obj):
#         return (request.user.is_authenticated
#                 and request.user.is_superuser)
