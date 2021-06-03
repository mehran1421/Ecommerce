from rest_framework.permissions import BasePermission, SAFE_METHODS


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


class IsSuperUserOrReadonly(BasePermission):
    """
      just superuser can change information
      use in:
      1-'create', 'update', 'destroy' Category : just superuser
      2-all Figure
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            # get access to superuser
            request.user.is_authenticated and
            request.user.is_superuser
        )


class IsSellerOrSuperUserObject(BasePermission):
    """
         just superuser or users that are owner product can change information
         use in:
         1-'update', 'destroy' Product : just superuser
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            # get access to superuser
            request.user.is_authenticated and
            (request.user.is_superuser or
             obj.seller == request.user)
        )
