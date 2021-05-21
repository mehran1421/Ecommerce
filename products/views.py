from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
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
from .pagination import PaginationTools
from .permissions import IsSuperUserOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


class ProductList(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = PaginationTools
    permission_classes = (IsSuperUserOrReadOnly,)

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 60))
    def dispatch(self, *args, **kwargs):
        return super(ProductList, self).dispatch(*args, **kwargs)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    queryset = Product.objects.all()
    permission_classes = (IsSuperUserOrReadOnly,)


class ProductCategory(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PaginationTools

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs.get('slug'))
        return Product.objects.filter(category=category)


class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = PaginationTools
    permission_classes = (IsSuperUserOrReadOnly,)

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 60))
    def dispatch(self, *args, **kwargs):
        return super(CategoryList, self).dispatch(*args, **kwargs)
