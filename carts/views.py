from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveDestroyAPIView
from .serializers import CartSerializers, CartItemSerializers
from .models import Cart, CartItem
from rest_framework.response import Response


class CartListApi(ListAPIView):
	queryset = Cart.objects.all()
	serializer_class = CartSerializers


class CartListCreateApi(ListCreateAPIView):
	serializer_class = CartSerializers

	def get_queryset(self):
		return Cart.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		return serializer.save(user=self.request.user)


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

	def get_object(self):
		queryset = CartItem.objects.filter(id=self.kwargs['pk']).first()
		return queryset

	def perform_destroy(self, instance):
		instance = self.get_object()
		if instance.cart.user != self.request.user:
			return Response("Cannot delete default system category",status=403)
		return instance.delete()
