from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
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
            obj = CartItem.objects.all()
            obj_cart = Cart.objects.all()
            cart_obj = obj_cart.filter(user=request.user).first()
            query = obj.filter(cart=cart_obj)
            serializer = CartItemListSerializers(query, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        try:
            obj = CartItem.objects.all()
            obj_cart = Cart.objects.all()
            cart_obj = obj_cart.filter(user=request.user).first()
            queryset = obj.filter(pk=pk, cart=cart_obj)
            serializer = CartItemDetailSerializers(queryset, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        try:
            obj = CartItem.objects.all()
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
        obj_cart = Cart.objects.all()
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
        obj = CartItem.objects.all()
        obj_cart = Cart.objects.all()
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
        obj = Cart.objects.all()
        try:
            queryset = obj.filter(is_pay=False)
            serializer = CartListSerializers(queryset, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        obj = Cart.objects.all()
        try:
            if request.user.is_superuser:
                cart = obj.filter(is_pay=False, pk=pk)
            else:
                cart = obj.filter(is_pay=False, user=request.user, pk=pk)
            serializer = CartDetailSerializers(cart, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        obj = Cart.objects.all()
        try:
            if request.user.is_superuser:
                cart = obj.get(is_pay=False, pk=pk)
            else:
                cart = obj.get(is_pay=False, user=request.user, pk=pk)
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
                    serializer.save(is_pay=False, user=request.user)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def update(self, request, pk=None):
        obj = Cart.objects.all()
        try:
            if request.user.is_superuser:
                cart = obj.get(is_pay=False, pk=pk)
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
