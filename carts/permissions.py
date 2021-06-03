from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):
    """
        use in:
        1-list Cart: just superuser can see list carts
    """

    def has_permission(self, request, view):
        return bool(
            # get access to superuser
            request.user.is_authenticated and
            request.user.is_superuser
        )


class IsSuperUserOrSelfObject(BasePermission):
    """
           use in:
           1-create,update,destroy CartItem: superuser or user that owner object can change it
           2-retrieve,destroy,update Cart: ...
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_superuser or
            obj.cart.user == request.user
        )
