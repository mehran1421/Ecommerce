from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOrIsSellerOrReadOnly(BasePermission):
    """
    for create product,
    just superuser or seller
    """

    def has_permission(self, request, view):
        return bool(
            # get access to superuser
            request.user.is_authenticated and
            request.user.is_superuser or
            request.user.is_seller
        )


class IsSuperUserOrIsSellerProductOrReadOnly(BasePermission):
    """
    for delete or update product,just superuser or product seller
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and
            request.user.is_superuser or
            obj.seller == request.user
        )
