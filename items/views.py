from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from extension.utils import cacheProduct
from django.db.models import Q
from .permissions import (
    IsSuperUserOrIsSeller,
    IsSuperUserOrReadonly,
    IsSellerOrSuperUserObject
)
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    InputProductSerializers,
    CategoryListSerializer,
    CategoryInputSerializer,
    CategoryDetailSerializer,
    FigureFieldSerializer,
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
            permission_classes = (IsSellerOrSuperUserObject,)

        return [permission() for permission in permission_classes]

    lookup_field = 'slug'

    def list(self, request):
        """
               for superuser return all object and
               for other user return Objects that status=True,choice='p'
               :param request:
               :return:
        """
        obj = cacheProduct(request, 'products', Product)
        if not request.user.is_superuser:
            product = obj.filter(status=True, choice='p')
        else:
            product = obj
        serializer = ProductSerializer(product, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
                create object and put choice='d',status=False,seller=request.user
                and superuser must ok object ====> status=True,choice='p' for shows site
                :param request:
                :return:
        """
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
        """
               superuser can see all object detail
               but other user just objects that status=True,choice='p'
               :param request:
               :param slug:
               :return:
        """
        obj = cacheProduct(request, 'products', Product)
        if not request.user.is_superuser:
            queryset = obj.filter(slug=slug, status=True, choice='p')
        else:
            queryset = obj
        serializer = ProductDetailSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def update(self, request, slug=None):
        """
               superuser can change all objects
               but other user if is_seller=True and be seller object just can change owner object
               if other user update object status=False,choice='d' for dont show site
               :param request:
               :param slug:
               :return:
        """
        obj = cacheProduct(request, 'products', Product)
        if request.user.is_superuser:
            product = obj.get(slug=slug)
        else:
            product = obj.get(slug=slug, seller=request.user)

        serializer = ProductDetailSerializer(product, data=request.data)
        if serializer.is_valid():
            if request.user.is_superuser:
                serializer.save()
            else:
                serializer.save(choice='d', status=False, seller=request.user)
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, slug=None):
        """
                superuser can delete all objects
                but other user if is_seller=True and be seller object just can delete owner object
                :param request:
                :param slug:
                :return:
        """
        obj = cacheProduct(request, 'products', Product)
        if request.user.is_superuser:
            product = obj.get(slug=slug)
        else:
            product = obj.get(slug=slug, seller=request.user)
        product.delete()
        return Response({'status': 'ok'}, status=200)

    @action(detail=False, methods=['get'], name='items-search')
    def product_search(self, request):
        # http://localhost:8000/product/product_search/?search=mehran
        obj = cacheProduct(request, 'products', Product)
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
        """
               list all category
               :param request:
               :return:
        """
        obj = cacheProduct(request, 'category', Category)
        category = obj.filter(status=True)
        serializer = CategoryListSerializer(category, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        """
                detail category
                :param request:
                :param slug:
                :return:
        """
        obj = cacheProduct(request, 'category', Category)
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
        """
              update category
              :param request:
              :param slug:
              :return:
        """
        category = Category.objects.get(slug=slug)
        serializer = CategoryDetailSerializer(category, data=request.data)
        if serializer.is_valid() and request.user.is_superuser:
            serializer.save()
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, slug=None):
        """
                delete object
                :param request:
                :param slug:
                :return:
        """
        category = Category.objects.get(slug=slug)
        if request.user.is_superuser:
            category.delete()
        return Response({'status': 'ok'}, status=200)

    @action(detail=True, methods=['get'], name='product-cat')
    def product_category(self, request, slug=None):
        """
              all products that in this category
              for example user click to mobile category and shows to user all products that be mobile category
              :param request:
              :param slug:
              :return:
        """
        obj = cacheProduct(request, 'category', Category)
        pro_obj = cacheProduct(request, 'products', Product)
        queryset = obj.filter(slug=slug, status=True).first()
        products = pro_obj.filter(category=queryset)
        serializer = ProductSerializer(products, context={'request': request}, many=True)
        return Response(serializer.data)


class FigureViews(ViewSet):
    """
       figure fields for example:
       os:""
       color:""
       and ...
    """
    permission_classes = (IsSuperUserOrReadonly,)

    def list(self, request):
        obj = cacheProduct(request, 'figure', FigureField)
        serializer = FigureFieldSerializer(obj, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = cacheProduct(request, 'figure', FigureField)
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
        obj = cacheProduct(request, 'figure', FigureField)
        figure = obj.get(pk=pk)
        serializer = FigureFieldSerializer(figure, data=request.data)
        if serializer.is_valid() and request.user.is_superuser:
            serializer.save()
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, pk=None):
        """
               delete figure field
               :param request:
               :param pk:
               :return:
        """
        obj = cacheProduct(request, 'figure', FigureField)
        figure = obj.get(pk=pk)
        if request.user.is_superuser:
            figure.delete()
        return Response({'status': 'ok'}, status=200)
