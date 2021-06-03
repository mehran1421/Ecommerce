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
from .permissions import (
    IsSuperUserOrSelfObject,
    IsSuperUser)
from .models import (
    Cart,
    CartItem
)


class CartItemViews(ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrSelfObject,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart_obj = obj.get(is_pay=False)
            query = cacheCartItem(request, f'cartItem-{cart_obj.user.email}', CartItem, cart_obj)
            serializer = CartItemListSerializers(query, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart_obj = obj.get(is_pay=False)
            cart_items = cacheCartItem(request, f'cartItem-{cart_obj.user.email}', CartItem, cart_obj)
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
        try:
            obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
            cart = obj.get(is_pay=False)
            cart_items = cacheCartItem(request, f'cartItem-{cart.user.email}', CartItem, cart)
            queryset = cart_items.get(pk=pk)
            serializer = CartItemDetailSerializers(queryset, data=request.data)
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
        else:
            permission_classes = ()
        return [permission() for permission in permission_classes]

    def list(self, request):
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
