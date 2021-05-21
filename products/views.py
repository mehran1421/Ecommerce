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

    