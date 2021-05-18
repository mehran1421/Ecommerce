from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            # get access to superuser
            request.user.is_authenticated and
            request.user.is_superuser
        )


class IsSuperUserOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_superuser or
            obj.cart.user == request.user
        )
