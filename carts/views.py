from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveDestroyAPIView
from .serializers import CartSerializers, CartItemSerializers
from .models import Cart, CartItem


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
		pk=self.kwargs.get('pk')
		return CartItem.objects.get(pk=pk)


