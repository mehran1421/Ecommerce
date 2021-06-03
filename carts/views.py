from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from extension.utils import cacheCart, cacheCartItem
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CartItemListSerializers,
    CartItemDetailSerializers,
    CartItemInputSerializers,
    CartListSerializers,
    CartDetailSerializers,
    CartInputSerializers
)
from .permissions import (
    IsSuperUserOrSelfObject,
    IsSuperUser)
from .models import (
    Cart,
    CartItem
)


class CartItemViews(ViewSet):
    """
        users can list,retrieve,update,destroy,create object for each cart
    """

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrSelfObject,)
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
            obj = cacheCartItem(request, 'cartItem-list', CartItem)
            obj_cart = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            if request.user.is_superuser:
                query = obj
            else:
                cart_obj = obj_cart.filter(user=request.user, is_pay=False).first()
                query = obj.filter(cart=cart_obj)
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
            obj = cacheCartItem(request, 'cartItem-list', CartItem)
            obj_cart = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            if request.user.is_superuser:
                queryset = obj.filter(pk=pk)
            else:
                cart_obj = obj_cart.filter(user=request.user, is_pay=False).first()
                queryset = obj.filter(pk=pk, cart=cart_obj)
            serializer = CartItemDetailSerializers(queryset, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        try:
            obj = cacheCartItem(request, 'cartItem-list', CartItem)
            obj_cart = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            if request.user.is_superuser:
                cart_item = obj.get(pk=pk)
            else:
                cart = obj_cart.get(user=request.user, is_pay=False)
                cart_item = obj.get(pk=pk, cart=cart)

            cart_item.delete()
            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def create(self, request):
        """
                when create owner user is request.user and is_pay=False
                :param request:
                :return:
        """
        obj_cart = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
        try:
            serializer = CartItemInputSerializers(data=request.data)
            cart = obj_cart.get(user=request.user, is_pay=False)
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
        obj = cacheCartItem(request, 'cartItem-list', CartItem)
        obj_cart = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
        try:
            if request.user.is_superuser:
                cartItem = obj.get(pk=pk)
            else:
                cart = obj_cart.get(user=request.user, is_pay=False)
                cartItem = obj.get(cart=cart)

            serializer = CartItemDetailSerializers(cartItem, data=request.data)
            if serializer.is_valid():
                if request.user.is_superuser:
                    serializer.save()
                else:
                    serializer.save(cart=cart)
                return Response({'status': 'ok'}, status=200)
            return Response({'status': 'Internal Server Error'}, status=500)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)


class CartViews(ViewSet):
    def get_permissions(self):
        if self.action in ['retrieve', 'destroy', 'update']:
            permission_classes = (IsSuperUserOrSelfObject,)
        elif self.action == 'list':
            permission_classes = (IsSuperUser,)
        else:
            permission_classes = ()
        return [permission() for permission in permission_classes]

    def list(self, request):
        """
               other user can show list carts that is_pay=False
               :param request:
               :return:
        """
        obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
        try:
            if request.user.is_superuser:
                queryset = Cart.objects.filter(is_pay=False)
            else:
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
        obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
        try:
            if request.user.is_superuser:
                cart = Cart.objects.filter(pk=pk)
            else:
                cart = obj.filter(is_pay=False, user=request.user, pk=pk)
            serializer = CartDetailSerializers(cart, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
        try:
            if request.user.is_superuser:
                cart = Cart.objects.get(pk=pk)
            else:
                cart = obj.get(is_pay=False, user=request.user, pk=pk)
            cart.delete()
            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def create(self, request):
        """
                when create object user=request.user and is_pay=False
                :param request:
                :return:
        """
        try:
            cart = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            lenCart = cart.objects.filter(is_pay=False).count()
            serializer = CartInputSerializers(data=request.data)
            if serializer.is_valid() and lenCart == 0:
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
        obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
        try:
            if request.user.is_superuser:
                cart = Cart.objects.get(pk=pk)
            else:
                cart = obj.get(is_pay=False, user=request.user, pk=pk)

            serializer = CartDetailSerializers(cart, data=request.data)
            if serializer.is_valid():
                if request.user.is_superuser:
                    serializer.save()
                else:
                    serializer.save(user=request.user)
                return Response({'status': 'ok'}, status=200)
            return Response({'status': 'Internal Server Error'}, status=500)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)
