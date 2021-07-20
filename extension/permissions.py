from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOrOwnerCart(BasePermission):
    """
        use in:
        1-create,update,destroy CartItem: superuser or user that owner object can change it
        2-retrieve,destroy,update Cart: ...
    """

    def has_permission(self, request, view):
        return bool(
            # get access to superuser
            request.user.is_authenticated and
            request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_superuser or
            obj.cart.user == request.user
        )


class IsSuperUserOrIsSeller(BasePermission):
    """
    for create product,
    just superuser or seller
    use in:
    create product : just superuser or is_seller user equals True
    """

    def has_permission(self, request, view):
        return bool(
            # get access to superuser
            request.user.is_authenticated and
            (request.user.is_superuser or
             request.user.is_seller)
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            # get access to superuser
            request.user.is_authenticated and
            (request.user.is_superuser or
             obj.seller == request.user)
        )