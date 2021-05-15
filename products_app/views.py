from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from .serializers import ProductSerializer, CategorySerializer, ProductDetailSerializer
from .models import Product, Category


class ProductList(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetail(RetrieveUpdateAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    queryset = Product.objects.all()


class ProductCategory(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs.get('slug'))
        return Product.objects.filter(category=category)


class CategoryList(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
