from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveDestroyAPIView
# from .serializers import CartSerializers, CartItemSerializers
from .models import Cart, CartItem
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from .permissions import IsSuperUser, IsSuperUserOrSelfObject
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import CartItemListSerializers, CartItemDetailSerializers
from users.models import User


class CartItemViews(ViewSet):
    def list(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        cartItem = CartItem.objects.filter(cart=cart)
        serializer = CartItemListSerializers(cartItem, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        cart = Cart.objects.filter(user=request.user).first()
        queryset = CartItem.objects.filter(cart=cart, pk=pk)
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

#
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
