from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveDestroyAPIView
from .serializers import CartSerializers, CartItemSerializers
from .models import Cart, CartItem
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from .permissions import IsSuperUser, IsSuperUserOrSelf


class CartPayListApi(ListAPIView):
    queryset = Cart.objects.filter(is_pay=True)
    serializer_class = CartSerializers
    permission_classes = (IsSuperUser,)

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 60))
    def dispatch(self, *args, **kwargs):
        return super(CartPayListApi, self).dispatch(*args, **kwargs)


class CartListCreateApi(ListCreateAPIView):
    serializer_class = CartSerializers
    permission_classes = (IsSuperUserOrSelf,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Cart.objects.all()
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 60))
    def dispatch(self, request, *args, **kwargs):
        return super(CartListCreateApi, self).dispatch(*args, **kwargs)


class CartItemCreateApi(ListCreateAPIView):
    serializer_class = CartItemSerializers

    def get_queryset(self):
        global cart
        cart = Cart.objects.filter(user=self.request.user).first()
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        return serializer.save(cart=cart)


class CartItemDeleteApi(RetrieveDestroyAPIView):
    serializer_class = CartItemSerializers
    lookup_field = 'pk'
    permission_classes = (IsSuperUserOrSelf,)

    def get_object(self):
        queryset = CartItem.objects.filter(id=self.kwargs['pk']).first()
        return queryset

    def perform_destroy(self, instance):
        instance = self.get_object()
        if instance.cart.user != self.request.user:
            return Response("Cannot delete default system category", status=403)
        return instance.delete()
