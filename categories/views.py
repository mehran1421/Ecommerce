from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from extension.utils import cacheops
from products.permissions import IsSuperUserOrReadonly
from products.serializers import ProductSerializer
from products.models import Product
from .serializers import (
    CategoryListSerializer,
    CategoryInputSerializer,
    CategoryDetailSerializer,
    FigureFieldSerializer,
)
from .models import (
    Category,
    FigureField
)


class CategoryViews(ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrReadonly,)
        else:
            permission_classes = ()
        return [permission() for permission in permission_classes]

    lookup_field = 'slug'

    def list(self, request):
        obj = cacheops(request, 'category-list', Category)
        category = obj.filter(status=True)
        serializer = CategoryListSerializer(category, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        obj = cacheops(request, 'category-list', Category)
        queryset = obj.filter(slug=slug, status=True)
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
        obj = cacheops(request, 'category-list', Category)
        pro_obj = cacheops(request, 'product-list', Product)
        queryset = obj.filter(slug=slug, status=True).first()
        products = pro_obj.filter(category=queryset)
        serializer = ProductSerializer(products, context={'request': request}, many=True)
        return Response(serializer.data)


class FigureViews(ViewSet):
    permission_classes = (IsSuperUserOrReadonly,)

    def list(self, request):
        obj = cacheops(request, 'figure-list', FigureField)
        serializer = FigureFieldSerializer(obj, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = cacheops(request, 'figure-list', FigureField)
        queryset = obj.filter(pk=pk)
        serializer = FigureFieldSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = FigureFieldSerializer(data=request.data)
            if serializer.is_valid() and request.user.is_superuser:
                serializer.save()
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def update(self, request, pk=None):
        figure = FigureField.objects.get(pk=pk)
        serializer = FigureFieldSerializer(figure, data=request.data)
        if serializer.is_valid() and request.user.is_superuser:
            serializer.save()
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, pk=None):
        figure = FigureField.objects.get(pk=pk)
        if request.user.is_superuser:
            figure.delete()
        return Response({'status': 'ok'}, status=200)
