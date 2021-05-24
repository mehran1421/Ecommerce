from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.cache import cache
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


def cacheops(request, name, model):
    obj = cache.get(name, None)
    if obj is None:
        obj = model.objects.all()
        cache.set(name, obj)
    return obj


class CartItemViews(ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrSelfObject,)
        else:
            permission_classes = ()
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            obj = cacheops(request, 'cartItem-list', CartItem)
            obj_cart = cacheops(request, 'cart-list', Cart)
            cart_obj = obj_cart.filter(user=request.user).first()
            query = obj.filter(cart=cart_obj)
            serializer = CartItemListSerializers(query, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        try:
            obj = cacheops(request, 'cartItem-list', CartItem)
            obj_cart = cacheops(request, 'cart-list', Cart)
            cart_obj = obj_cart.filter(user=request.user).first()
            queryset = obj.filter(pk=pk, cart=cart_obj)
            serializer = CartItemDetailSerializers(queryset, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        try:
            obj = cacheops(request, 'cartItem-list', CartItem)
            obj_cart = cacheops(request, 'cart-list', Cart)
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
        obj_cart = cacheops(request, 'cart-list', Cart)
        try:
            serializer = CartItemInputSerializers(data=request.data)
            cart = obj_cart.get(user=request.user)
            if serializer.is_valid():
                serializer.save(cart=cart)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def update(self, request, pk=None):
        obj = cacheops(request, 'cartItem-list', CartItem)
        obj_cart = cacheops(request, 'cart-list', Cart)
        try:
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
        obj = cacheops(request, 'cart-list', Cart)
        try:
            serializer = CartListSerializers(obj, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        obj = cacheops(request, 'cart-list', Cart)
        try:
            if request.user.is_superuser:
                cart = obj.filter(pk=pk)
            else:
                cart = obj.filter(user=request.user, pk=pk)
            serializer = CartDetailSerializers(cart, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        obj = cacheops(request, 'cart-list', Cart)
        try:
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
            serializer = CartInputSerializers(data=request.data)
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
        obj = cacheops(request, 'cart-list', Cart)
        try:
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
