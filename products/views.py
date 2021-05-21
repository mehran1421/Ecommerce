from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ProductDetailSerializer
)
from .models import (
    Product,
    Category
)
from users.models import User
from .pagination import PaginationTools
from .permissions import IsSuperUserOrIsSellerOrReadOnly, IsSuperUserOrIsSellerProductOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


class ProductViews(ViewSet):
    # def get_permissions(self):
    #     if self.action == 'create':
    #         return IsSuperUserOrIsSellerOrReadOnly
    #     elif self.action == 'retrieve':
    #         return IsSuperUserOrIsSellerProductOrReadOnly
    # @method_decorator(cache_page(60 * 60 * 2))
    # @method_decorator(vary_on_cookie)
    lookup_field = 'slug'

    def list(self, request):
        queryset = Product.objects.filter(status=True, choice='p')
        serializer = ProductSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    # @method_decorator(cache_page(60 * 60 * 2))
    # @method_decorator(vary_on_cookie)
    def retrieve(self, request, slug=None):
        queryset = Product.objects.filter(slug=slug, status=True, choice='p')
        serializer = ProductDetailSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def update(self, request, slug=None):
        product = Product.objects.get(slug=slug)
        print(product)
        serializer = ProductDetailSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, slug=None):
        product = Product.objects.get(slug=slug)
        product.delete()
        return Response({'status': 'ok'}, status=200)


class CategoryViews(ViewSet):
    # def get_permissions(self):
    #     if self.action == 'create':
    #         return IsSuperUserOrIsSellerOrReadOnly
    #     elif self.action == 'retrieve':
    #         return IsSuperUserOrIsSellerProductOrReadOnly
    # @method_decorator(cache_page(60 * 60 * 2))
    # @method_decorator(vary_on_cookie)
    lookup_field = 'slug'

    def list(self, request):
        queryset = Category.objects.filter(status=True)
        serializer = CategorySerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def update(self, request, slug=None):
        category = Category.objects.get(slug=slug)
        serializer = ProductDetailSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, slug=None):
        category = Category.objects.get(slug=slug)
        category.delete()
        return Response({'status': 'ok'}, status=200)
