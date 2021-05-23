from .models import Cart, CartItem
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.cache import cache
from .serializers import CartItemListSerializers, CartItemDetailSerializers, CartListSerializers, CartDetailSerializers
from users.models import User


class CartItemViews(ViewSet):
    def list(self, request):
        obj = cache.get('cartItem-list', None)
        cart = Cart.objects.all()
        cart_obj = cart.filter(user=request.user).first()
        if obj is None:
            obj = CartItem.objects.filter(cart=cart_obj)
            cache.set('cart-list', cart)
            cache.set('cartItem-list', obj)

        serializer = CartItemListSerializers(obj, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = cache.get('cartItem-list', None)
        cart_cache = cache.get('cart-list', None)
        if cart_cache is None:
            cart = Cart.objects.all()
            cache.set('cart-list', cart)
            cart_obj = cart.filter(user=request.user).first()
        else:
            cart_obj = cart_cache.filter(user=request.user).first()

        if obj is None:
            obj = CartItem.objects.filter(cart=cart_obj)
            cache.set('cartItem-list', obj)
        queryset = obj.filter(pk=pk)
        serializer = CartItemDetailSerializers(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        if request.user.is_superuser:
            cart_item = CartItem.objects.get(pk=pk)
        else:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(pk=pk, cart=cart)

        cart_item.delete()
        return Response({'status': 'ok'}, status=200)

    def create(self, request):
        try:
            serializer = CartItemDetailSerializers(data=request.data)
            cart = Cart.objects.get(user=request.user)
            if serializer.is_valid():
                serializer.save(cart=cart)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def update(self, request, pk=None):
        if request.user.is_superuser:
            cartItem = CartItem.objects.get(pk=pk)
        else:
            cart = Cart.objects.get(user=request.user)
            cartItem = CartItem.objects.get(cart=cart)

        serializer = CartItemDetailSerializers(cartItem, data=request.data)
        if serializer.is_valid():
            if request.user.is_superuser:
                serializer.save()
            else:
                serializer.save(cart=cart)
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)


class CartViews(ViewSet):
    def list(self, request):
        if request.user.is_superuser:
            cart = Cart.objects.all()
        else:
            cart = Cart.objects.filter(user=request.user)
        serializer = CartListSerializers(cart, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if request.user.is_superuser:
            cart = Cart.objects.filter(pk=pk)
        else:
            cart = Cart.objects.filter(user=request.user, pk=pk)
        serializer = CartDetailSerializers(cart, context={'request': request}, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        if request.user.is_superuser:
            cart = Cart.objects.get(pk=pk)
        else:
            cart = Cart.objects.get(user=request.user, pk=pk)

        cart.delete()
        return Response({'status': 'ok'}, status=200)

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
        if request.user.is_superuser:
            cart = Cart.objects.get(pk=pk)
        else:
            cart = Cart.objects.get(user=request.user, pk=pk)

        serializer = CartDetailSerializers(cart, data=request.data)
        if serializer.is_valid():
            if request.user.is_superuser:
                serializer.save()
            else:
                serializer.save(user=request.user)
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

# class CartPayListApi(ListAPIView):
#     '''
#     To show the members who have paid
#     '''
#     queryset = Cart.objects.filter(is_pay=True)
#     serializer_class = CartSerializers
#     # just show to superuser
#     permission_classes = (IsSuperUser,)
#     ordering = ['-timestamp']
#     # localhost:8000/cart/all/?search= mehran
#     search_fields = ['user__username', 'user__first_name', 'user__last_name', 'is_pay']
#     # localhost:8000/cart/all/?ordering=-timestamp
#     ordering_fields = ['timestamp']
#
#     # for cache
#     @method_decorator(vary_on_cookie)
#     @method_decorator(cache_page(60 * 60))
#     def dispatch(self, *args, **kwargs):
#         return super(CartPayListApi, self).dispatch(*args, **kwargs)
#
#
# class CartListCreateApi(ListCreateAPIView):
#     '''
#     create and show cart object
#     '''
#     serializer_class = CartSerializers
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return Cart.objects.all()
#         return Cart.objects.filter(user=self.request.user)
#
#     def perform_create(self, serializer):
#         return serializer.save(user=self.request.user)
#
#     @method_decorator(vary_on_cookie)
#     @method_decorator(cache_page(60 * 60))
#     def dispatch(self, *args, **kwargs):
#         return super(CartListCreateApi, self).dispatch(*args, **kwargs)
#
#
# class CartItemCreateApi(ListCreateAPIView):
#     '''
#     each cart have many cart item
#     '''
#     serializer_class = CartItemSerializers
#
#     def get_queryset(self):
#         global cart
#         cart = Cart.objects.filter(user=self.request.user).first()
#         return CartItem.objects.filter(cart=cart)
#
#     def perform_create(self, serializer):
#         return serializer.save(cart=cart)
#
#
# class CartItemDeleteApi(RetrieveDestroyAPIView):
#     '''
#     delete cart item
#     '''
#     serializer_class = CartItemSerializers
#     queryset = CartItem.objects.all()
#     lookup_field = 'pk'
#     permission_classes = (IsSuperUserOrSelfObject,)
