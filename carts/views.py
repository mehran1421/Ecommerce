from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView
from .serializers import CartSerializers
from .models import Cart


class CartListApi(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers


class CartListCreateApi(ListCreateAPIView):
    serializer_class = CartSerializers

    def get_queryset(self):
        return Cart.objects.all()
