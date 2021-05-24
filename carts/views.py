from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.cache import cache
from .serializers import (
    CartItemListSerializers,
    CartItemDetailSerializers,
    CartListSerializers,
    CartDetailSerializers
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
            permission_classes = ()
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            obj = cache.get('cartItem-list', None)
            cart = Cart.objects.all()
            cart_obj = cart.filter(user=request.user).first()
            if obj is None:
                obj = CartItem.objects.all()
                cache.set('cart-list', cart)
                cache.set('cartItem-list', obj)
            query = obj.filter(cart=cart_obj)
            serializer = CartItemListSerializers(query, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        try:
            obj = cache.get('cartItem-list', None)
            cart_cache = cache.get('cart-list', None)
            if cart_cache is None:
                cart = Cart.objects.all()
                cache.set('cart-list', cart)
                cart_obj = cart.filter(user=request.user).first()
            else:
                cart_obj = cart_cache.filter(user=request.user).first()

            if obj is None:
                obj = CartItem.objects.all()
                cache.set('cartItem-list', obj)
            queryset = obj.filter(pk=pk, cart=cart_obj)
            serializer = CartItemDetailSerializers(queryset, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        try:
            obj = cache.get('cartItem-list', None)
            obj_cart = cache.get('cart-list', None)
            if obj is None:
                obj = CartItem.objects.all()

            if obj_cart is None:
                obj_cart = Cart.objects.all()

            if request.user.is_superuser:
                cart_item = obj.get(pk=pk)
            else:
                cart = obj_cart.get(user=request.user)
                cart_item = obj.get(pk=pk, cart=cart)

            cart_item.delete()
            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def create(self, request):
        obj_cart = cache.get('cart-list', None)
        if obj_cart is None:
            obj_cart = Cart.objects.all()
        try:
            serializer = CartItemDetailSerializers(data=request.data)
            cart = obj_cart.get(user=request.user)
            if serializer.is_valid():
                serializer.save(cart=cart)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def update(self, request, pk=None):
        try:
            obj = cache.get('cartItem-list', None)
            obj_cart = cache.get('cart-list', None)
            if obj is None:
                obj = CartItem.objects.all()

            if obj_cart is None:
                obj_cart = Cart.objects.all()

            if request.user.is_superuser:
                cartItem = obj.get(pk=pk)
            else:
                cart = obj_cart.get(user=request.user)
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
        try:
            obj = cache.get('cart-list', None)
            if obj is None:
                obj = Cart.objects.all()
                cache.set('cart-list', obj)
        
            cart = obj
            serializer = CartListSerializers(cart, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        try:
            obj = cache.get('cart-list', None)
            if obj is None:
                obj = Cart.objects.all()
                cache.set('cart-list', obj)
            if request.user.is_superuser:
                cart = obj.filter(pk=pk)
            else:
                cart = obj.filter(user=request.user, pk=pk)
            serializer = CartDetailSerializers(cart, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        try:
            obj = cache.get('cart-list', None)
            if obj is None:
                obj = Cart.objects.all()
            if request.user.is_superuser:
                cart = obj.get(pk=pk)
            else:
                cart = obj.get(user=request.user, pk=pk)
            cart.delete()
            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def create(self, request):
        try:
            serializer = CartDetailSerializers(data=request.data)
            if serializer.is_valid():
                if request.user.is_superuser:
                    serializer.save()
                else:
                    serializer.save(user=request.user)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def update(self, request, pk=None):
        try:
            obj = cache.get('cart-list', None)
            if obj is None:
                obj = Cart.objects.all()
            if request.user.is_superuser:
                cart = obj.get(pk=pk)
            else:
                cart = obj.get(user=request.user, pk=pk)

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
