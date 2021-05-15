from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView
)
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ProductDetailSerializer
)
from .models import (
    Product,
    Category
)
from .pagination import CategoryPagination, ProductPagination
from .permissions import IsSuperUserOrReadOnly


class ProductList(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = ProductPagination
    permission_classes = (IsSuperUserOrReadOnly,)


class ProductDetail(RetrieveUpdateAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    queryset = Product.objects.all()
    permission_classes = (IsSuperUserOrReadOnly,)


class ProductCategory(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs.get('slug'))
        return Product.objects.filter(category=category)


class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = CategoryPagination
    permission_classes = (IsSuperUserOrReadOnly,)
