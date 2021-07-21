from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from extension.utils import cacheCart, cacheCartItem
from extension.exception import CustomException
from extension import response
from .serializers import (
    CartItemListSerializers,
    CartItemDetailSerializers,
    CartItemInputSerializers,
    CartListSerializers,
    CartDetailSerializers,
    CartInputSerializers
)
from extension.permissions import (
    CartItemOwnerCartOrSuperuser,
    OwnerCartOrSuperuser
)
from .models import (
    Cart,
    CartItem
)


class CartItemViews(ViewSet):
    """
    users can list,retrieve,update,destroy,create object for each cart
    use caching with redis and database cache
    cacheCart ==> extension/utils.py ==> cache in redis by email user
    cacheCartItem ==> extension/utils.py ==> cache in redis by email user

    """

    def get_permissions(self):
        """
        IsSuperUserOrOwnerCart ==> if cartItem object have request.user or user is superuser
        :return:
        """
        if self.action in ['update', 'destroy']:
            permission_classes = (CartItemOwnerCartOrSuperuser,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        other user can just see self cartItems object
        show user CartItem list for your cart
        :param request:
        :return:
        """
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            # this is for select is_pay = False object, that means thay that dont payment
            cart_obj = obj.filter(is_pay=False).first()

            # this is for select CartItem objects that are in user cart that is_pay = False
            query = cacheCartItem(request, f'cartItem-{cart_obj.user.email}', CartItem, cart_obj)
            serializer = CartItemListSerializers(query, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def retrieve(self, request, pk=None):
        """
        detail cartItem for other user
        :param request:
        :param pk:
        :return:
        """
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)

            # this is for select is_pay = False object, that means thay that dont payment
            cart_obj = obj.get(is_pay=False)
            cart_items = cacheCartItem(request, f'cartItem-{cart_obj.user.email}', CartItem, cart_obj)

            # this is for select CartItem object that is in user cart that is_pay = False
            queryset = cart_items.get(pk=pk)
            serializer = CartItemDetailSerializers(queryset, context={'request': request})
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def destroy(self, request, pk=None):
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            # this is for select is_pay = False object, that means thay that dont payment
            cart = obj.get(is_pay=False)
            cart_items = cacheCartItem(request, f'cartItem-{cart.user.email}', CartItem, cart)

            # this is for select CartItem objects that are in user cart that is_pay = False
            queryset = cart_items.get(pk=pk)
            queryset.delete()
            return response.SuccessResponse(message='Delete object').send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def create(self, request):
        """
        when create owner user is request.user and is_pay=False
        create CartItem object for your cart that is_pay = False
        :param request:
        :return:
        """
        try:
            serializer = CartItemInputSerializers(data=request.data)

            # get user cart for add created object to your cart
            obj_cart = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart = obj_cart.get(is_pay=False)
            if serializer.is_valid():
                serializer.save(cart=cart)
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def update(self, request, pk=None):
        """
        user cant change cart in update
        :param request:
        :param pk:
        :return:
        """
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart = obj.get(is_pay=False)
            cart_items = cacheCartItem(request, f'cartItem-{cart.user.email}', CartItem, cart)
            queryset = cart_items.get(pk=pk)
            serializer = CartItemInputSerializers(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save(cart=cart)
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()


class CartViews(ViewSet):
    def get_permissions(self):
        """
        IsSuperUserOrOwnerCart ==> if cartItem object have request.user or user is superuser
        :return:
        """
        if self.action in ['retrieve', 'destroy', 'update']:
            permission_classes = (OwnerCartOrSuperuser,)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]

    def list(self, request):
        """
               other user can show list carts that is_pay=False
               show user just one cart that is_pay = False
               Indeed, user cant create more than one cart
               :param request:
               :return:
        """
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            queryset = obj.filter(is_pay=False)
            serializer = CartListSerializers(queryset, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def retrieve(self, request, pk=None):
        """
        detail cart
        :param request:
        :param pk:
        :return:
        """
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart = obj.get(is_pay=False, user=request.user, pk=pk)
            serializer = CartDetailSerializers(cart, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def destroy(self, request, pk=None):
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart = obj.filter(is_pay=False, user=request.user, pk=pk).first()
            cart.delete()
            return response.SuccessResponse(message='Delete object').send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def create(self, request):
        """
        when create object user=request.user and is_pay=False
        :param request:
        :return:
        """
        try:
            cart = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            len_cart = cart.filter(is_pay=False).count()
            serializer = CartInputSerializers(data=request.data)
            if serializer.is_valid():
                if len_cart == 0:
                    serializer.save(is_pay=False, user=request.user)
                    return response.SuccessResponse(serializer.data).send()
                else:
                    return response.ErrorResponse(message='cart object is_pay == False exist.', status=403).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def update(self, request, pk=None):
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart = obj.get(is_pay=False, user=request.user, pk=pk)
            serializer = CartInputSerializers(cart, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()
