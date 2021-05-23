from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from django.core.cache import cache
from users.models import User
from .pagination import PaginationTools
from .permissions import (
    IsSuperUserOrIsSeller,
    IsSuperUserOrReadonly
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


class ProductViews(ViewSet):
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = (IsSuperUserOrIsSeller,)
        elif self.action == 'list':
            permission_classes = ()
        else:
            permission_classes = (IsSuperUserOrReadonly,)

        return [permission() for permission in permission_classes]

    lookup_field = 'slug'

    def list(self, request):
        obj = cache.get('product-list', None)
        if obj is None:
            obj = Product.objects.filter(status=True, choice='p')
            cache.set('product-list', obj)
        serializer = ProductSerializer(obj, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(choice='d', status=False, seller=request.user)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def retrieve(self, request, slug=None):
        obj = cache.get('product-list', None)
        if obj is None:
            obj = Product.objects.filter(status=True, choice='p')
            cache.set('product-list', obj)
        queryset = obj.filter(slug=slug)
        serializer = ProductDetailSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def update(self, request, slug=None):
        print(self.action)
        if request.user.is_superuser:
            product = Product.objects.get(slug=slug)
        else:
            product = Product.objects.get(slug=slug, seller=request.user)

        serializer = ProductDetailSerializer(product, data=request.data)
        if serializer.is_valid():
            if request.user.is_superuser:
                serializer.save()
            else:
                serializer.save(choice='d', status=False, seller=request.user)
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, slug=None):
        if request.user.is_superuser:
            product = Product.objects.get(slug=slug)
        elif request.user.is_authenticated:
            product = Product.objects.get(slug=slug, seller=request.user)

        if product.seller == request.user or request.user.is_superuser:
            product.delete()
            return Response({'status': 'ok'}, status=200)
        else:
            return Response({'status': 'Bad Request'}, status=500)


class CategoryViews(ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrReadonly,)
        else:
            permission_classes = ()
        return [permission() for permission in permission_classes]

    lookup_field = 'slug'

    def list(self, request):
        global obj
        obj = cache.get('category-list', None)
        if obj is None:
            obj = Category.objects.filter(status=True)
            cache.set('category-list', obj)
        serializer = CategorySerializer(obj, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        queryset = obj.filter(slug=slug)
        serializer = CategorySerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid() and request.user.is_superuser:
                serializer.save()
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def update(self, request, slug=None):
        category = Category.objects.get(slug=slug)
        serializer = ProductDetailSerializer(category, data=request.data)
        if serializer.is_valid() and request.user.is_superuser:
            serializer.save()
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, slug=None):
        category = Category.objects.get(slug=slug)
        if request.user.is_superuser:
            category.delete()
        return Response({'status': 'ok'}, status=200)

    @action(detail=True, methods=['get'], name='product-cat')
    def product_category(self, request, slug=None):
        pro_obj = cache.get('product-list', None)
        queryset = obj.filter(slug=slug).first()
        if pro_obj is None:
            products = Product.objects.filter(category=queryset)
        else:
            products = pro_obj.filter(category=queryset)
        serializer = ProductSerializer(products, context={'request': request}, many=True)
        return Response(serializer.data)
