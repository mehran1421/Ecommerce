from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOrIsSeller(BasePermission):
    """
    for create product,
    just superuser or seller
    """

    def has_permission(self, request, view):
        return bool(
            # get access to superuser
            request.user.is_authenticated and
            (request.user.is_superuser or
             request.user.is_seller)
        )


class IsSuperUserOrReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            # get access to superuser
            request.user.is_authenticated and
            request.user.is_superuser
        )
