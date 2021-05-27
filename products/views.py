from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from extension.utils import cacheops
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

