from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from extension.utils import cacheCart, cacheCartItem
from .serializers import (
    CartItemListSerializers,
    CartItemDetailSerializers,
    CartItemInputSerializers,
    CartListSerializers,
    CartDetailSerializers,
    CartInputSerializers
)
from extension.permissions import (
    IsSuperUserOrOwnerCart
)
from .models import (
    Cart,
    CartItem
)


class CartItemViews(ViewSet):
    """
    users can list,retrieve,update,destroy,create object for each cart
    """

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            permission_classes = (IsSuperUserOrOwnerCart,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        other user can just see self cartItems object
        :param request:
        :return:
        """
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart_obj = obj.filter(is_pay=False).first()
            query = cacheCartItem(request, f'cartItem-{cart_obj.user.email}', CartItem, cart_obj)
            serializer = CartItemListSerializers(query, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        """
        detail cartItem for other user
        :param request:
        :param pk:
        :return:
        """
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart_obj = obj.get(is_pay=False)
            print(cart_obj)
            print("===========")
            cart_items = cacheCartItem(request, f'cartItem-{cart_obj.user.email}', CartItem, cart_obj)
            print(cart_items)
            print("///////////")
            queryset = cart_items.get(pk=pk)
            print(queryset)
            serializer = CartItemDetailSerializers(queryset, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart = obj.get(is_pay=False)
            cart_items = cacheCartItem(request, f'cartItem-{cart.user.email}', CartItem, cart)
            queryset = cart_items.get(pk=pk)

            queryset.delete()
            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def create(self, request):
        """
        when create owner user is request.user and is_pay=False
        :param request:
        :return:
        """
        try:
            serializer = CartItemInputSerializers(data=request.data)
            obj_cart = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart = obj_cart.get(is_pay=False)
            if serializer.is_valid():
                if request.user.is_superuser:
                    serializer.save()
                else:
                    serializer.save(cart=cart)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

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
                if request.user.is_superuser:
                    serializer.save()
                else:
                    serializer.save(cart=cart)
                return Response({'status': 'ok'}, status=200)
            return Response({'status': 'Internal Server Error'}, status=400)
        except Exception:
            return Response({'status': 'must you authentications '}, status=500)


class CartViews(ViewSet):
    def get_permissions(self):
        if self.action in ['retrieve', 'destroy', 'update']:
            permission_classes = (IsSuperUserOrOwnerCart,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def list(self, request):
        """
               other user can show list carts that is_pay=False
               :param request:
               :return:
        """
        try:
            if request.user.is_superuser:
                queryset = Cart.objects.filter(is_pay=False)
            else:
                obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
                queryset = obj.filter(is_pay=False)
            serializer = CartListSerializers(queryset, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        """
        detail cart
        :param request:
        :param pk:
        :return:
        """
        try:
            if request.user.is_superuser:
                cart = Cart.objects.get(pk=pk)
            else:
                obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
                cart = obj.get(is_pay=False, user=request.user, pk=pk)

            serializer = CartDetailSerializers(cart, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        try:
            if request.user.is_superuser:
                cart = Cart.objects.get(pk=pk, is_pay=False)
            else:
                obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
                cart = obj.filter(is_pay=False, user=request.user, pk=pk).first()
            cart.delete()
            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'error'}, status=400)

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
            if serializer.is_valid() and len_cart == 0:
                if request.user.is_superuser:
                    serializer.save()
                else:
                    serializer.save(is_pay=False, user=request.user)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def update(self, request, pk=None):
        try:
            if request.user.is_superuser:
                cart = Cart.objects.get(pk=pk)
            else:
                obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
                cart = obj.get(is_pay=False, user=request.user, pk=pk)

            serializer = CartInputSerializers(cart, data=request.data)
            if serializer.is_valid():
                if request.user.is_superuser:
                    serializer.save()
                else:
                    serializer.save(user=request.user)
                return Response({'status': 'ok'}, status=200)
            return Response({'status': 'Internal Server Error'}, status=400)
        except Exception:
            return Response({'status': 'must you authentications '}, status=500)
