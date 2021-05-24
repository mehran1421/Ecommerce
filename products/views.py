from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from users.models import User
from .pagination import PaginationTools
from django.db.models import Q
from .permissions import (
    IsSuperUserOrIsSeller,
    IsSuperUserOrReadonly
)
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    InputProductSerializers,
    CategoryDetailSerializer,
    CategoryListSerializer,
    CategoryInputSerializer,
    FigureFieldSerializer
)
from .models import (
    Product,
    Category,
    FigureField
)


def cacheops(request, name, model):
    obj = cache.get(name, None)
    if obj is None:
        obj = model.objects.all()
        cache.set(name, obj)
    return obj


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
        obj = cacheops(request, 'product-list', Product)
        product = obj.filter(status=True, choice='p')
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
        obj = cacheops(request, 'product-list', Product)
        queryset = obj.filter(slug=slug, status=True, choice='p')
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

    @action(detail=False, methods=['get'], name='products-search')
    def product_search(self, request):
        # http://localhost:8000/product/product_search/?search=mehran
        obj = cacheops(request, 'cart-list', Product)
        query = self.request.GET.get('search')
        object_list = obj.filter(
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
        obj = cacheops(request, 'category-list', Category)
        pro_obj = cacheops(request, 'product-list', Product)
        queryset = obj.filter(slug=slug, status=True).first()
        products = pro_obj.filter(category=queryset)
        serializer = ProductSerializer(products, context={'request': request}, many=True)
        return Response(serializer.data)


class FigureViews(ViewSet):
    def list(self, request):
        obj = cacheops(request, 'figure-list', FigureField)
        serializer = FigureFieldSerializer(obj, context={'request': request}, many=True)
        return Response(serializer.data)

