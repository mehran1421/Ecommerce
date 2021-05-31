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
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrSelfObject,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            if request.user.is_superuser:
                query = CartItem.objects.all()
            else:
                cart_obj = Cart.objects.filter(user=request.user, is_pay=False).first()
                query = CartItem.objects.filter(cart=cart_obj)
            serializer = CartItemListSerializers(query, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        try:
            if request.user.is_superuser:
                queryset = CartItem.objects.filter(pk=pk).first()
            else:
                cart_obj = Cart.objects.filter(user=request.user, is_pay=False).first()
                queryset = CartItem.objects.filter(pk=pk, cart=cart_obj)
            serializer = CartItemDetailSerializers(queryset, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        try:
            if request.user.is_superuser:
                cart_item = CartItem.objects.get(pk=pk)
            else:
                cart = Cart.objects.get(user=request.user, is_pay=False)
                cart_item = CartItem.objects.get(pk=pk, cart=cart)

            cart_item.delete()
            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def create(self, request):
        try:
            serializer = CartItemInputSerializers(data=request.data)
            cart = Cart.objects.get(user=request.user, is_pay=False)
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
            if request.user.is_superuser:
                cartItem = CartItem.objects.get(pk=pk)
            else:
                cart = Cart.objects.get(user=request.user, is_pay=False)
                cartItem = CartItem.objects.get(cart=cart)

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
            if request.user.is_superuser:
                queryset = Cart.objects.filter(is_pay=False)
            else:
                queryset = Cart.objects.filter(is_pay=False)
            serializer = CartListSerializers(queryset, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        try:
            if request.user.is_superuser:
                cart = Cart.objects.filter(is_pay=False, pk=pk).first()
            else:
                obj = cacheCart(request, f'cart-{request.user.email}', Cart, request.user)
                cart = Cart.objects.filter(is_pay=False, user=request.user, pk=pk).first()
            serializer = CartDetailSerializers(cart, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        try:
            if request.user.is_superuser:
                cart = Cart.objects.get(pk=pk)
            else:
                cart = Cart.objects.get(is_pay=False, user=request.user, pk=pk)
            cart.delete()
            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def create(self, request):
        try:
            cart = Cart.objects.filter(user=request.user,is_pay=False)
            lenCart = cart.count()
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
        try:
            if request.user.is_superuser:
                cart = Cart.objects.get(pk=pk)
            else:
                cart = Cart.objects.get(is_pay=False, user=request.user, pk=pk)

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
