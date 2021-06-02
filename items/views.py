import json
from rest_framework.viewsets import ViewSet
from items.serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from extension.utils import productCacheDatabase,cacheDetailProduct
from .permissions import (
    IsSuperUserOrIsSeller,
    IsSuperUserOrReadonly
)
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    InputProductSerializers,
    CategoryListSerializer,
    CategoryInputSerializer,
    CategoryDetailSerializer,
    FigureFieldSerializer,
    FigureFieldDetailSerializer
)
from .models import (
    Product,
    Category,
    FigureField,
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
        if request.user.is_superuser:
            product=Product.objects.all()
        else:
            product = productCacheDatabase(request, 'products', Product)
        serializer = ProductSerializer(product, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = InputProductSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(choice='d', status=False, seller=request.user)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def retrieve(self, request, slug=None):
        if request.user.is_superuser:
            queryset=Product.objects.get(slug=slug)
        else:
            queryset = cacheDetailProduct(request,f'product_{slug}',slug,Product)
        serializer = ProductDetailSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def update(self, request, slug=None):
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
        else:
            product = Product.objects.get(slug=slug, seller=request.user)
        product.delete()
        return Response({'status': 'ok'}, status=200)

    @action(detail=False, methods=['get'], name='items-search')
    def product_search(self, request):
        # http://localhost:8000/product/product_search/?search=mehran
        query = self.request.GET.get('search')
        object_list = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(price__iexact=query) |
            Q(category__title__icontains=query) |
            Q(seller__first_name__icontains=query) |
            Q(seller__username__icontains=query) |
            Q(seller__last_name__icontains=query),
            status=True,
            choice='p'
        )
        serializer = ProductSerializer(object_list, context={'request': request}, many=True)
        return Response(serializer.data)


class CategoryViews(ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrReadonly,)
        else:
            permission_classes = ()
        return [permission() for permission in permission_classes]

    lookup_field = 'slug'

    def list(self, request):
        category = Category.objects.filter(status=True)
        serializer = CategoryListSerializer(category, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        queryset = Category.objects.filter(slug=slug, status=True)
        serializer = CategoryDetailSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = CategoryInputSerializer(data=request.data)
            if serializer.is_valid() and request.user.is_superuser:
                serializer.save()
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def update(self, request, slug=None):
        category = Category.objects.get(slug=slug)
        serializer = CategoryDetailSerializer(category, data=request.data)
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
        queryset = Category.objects.filter(slug=slug, status=True).first()
        products = Product.objects.filter(category=queryset)
        serializer = ProductSerializer(products, context={'request': request}, many=True)
        return Response(serializer.data)


class FigureViews(ViewSet):
    permission_classes = (IsSuperUserOrReadonly,)

    def list(self, request):
        obj = FigureField.objects.all()
        serializer = FigureFieldSerializer(obj, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = FigureField.objects.get(pk=pk)
        serializer = FigureFieldDetailSerializer(queryset)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = FigureFieldDetailSerializer(data=request.data)
            if serializer.is_valid() and request.user.is_superuser:
                serializer.save()
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def update(self, request, pk=None):
        figure = FigureField.objects.get(pk=pk)
        serializer = FigureFieldDetailSerializer(figure, data=request.data)
        if serializer.is_valid() and request.user.is_superuser:
            serializer.save()
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, pk=None):
        figure = FigureField.objects.get(pk=pk)
        if request.user.is_superuser:
            figure.delete()
        return Response({'status': 'ok'}, status=200)
