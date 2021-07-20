from rest_framework.viewsets import ViewSet
from silk.profiling.profiler import silk_profile
from rest_framework.decorators import action
from django.db.models import Q
from extension.utils import productCacheDatabase, cacheDetailProduct, cacheCategoryOrFigur
from extension.permissions import IsSuperUserOrIsSeller, IsSuperUserOrOwnerCart

from extension.exception import CustomException

from extension import response
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
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrIsSeller,)
        else:
            permission_classes = ()

        return [permission() for permission in permission_classes]

    lookup_field = 'slug'

    def list(self, request):
        """
        for other user return Objects that status=True,choice='p'
        :param request:
        :return:
        """
        try:
            product = productCacheDatabase(request, 'products', Product)
            obj = product.filter(status=True, choice='p')
            serializer = ProductSerializer(obj, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    @silk_profile(name='create products')
    def create(self, request):
        """
        create object and put choice='d',status=False,seller=request.user
        and superuser must ok object ====> status=True,choice='p' for shows site
        :param request:
        :return:
        """
        try:
            serializer = InputProductSerializers(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(choice='d', status=False, seller=request.user)
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    @silk_profile(name='detail products')
    def retrieve(self, request, slug=None):
        """
               superuser can see all object detail
               but other user just objects that status=True,choice='p'
               :param request:
               :param slug:
               :return:
        """
        try:
            queryset = cacheDetailProduct(request, f'product_{slug}', slug, Product)
            serializer = ProductDetailSerializer(queryset, context={'request': request})
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    @silk_profile(name='update products')
    def update(self, request, slug=None):
        """
           superuser can change all objects
           but other user if is_seller=True and be seller object just can change owner object
           if other user update object status=False,choice='d' for dont show site
           :param request:
           :param slug:
           :return:
        """
        try:
            obj = productCacheDatabase(request, 'products', Product)
            product = obj.filter(slug=slug)
            serializer = ProductDetailSerializer(product, data=request.data)
            if serializer.is_valid(raise_exception=True):
                if request.user.is_superuser:
                    serializer.save()
                else:
                    serializer.save(choice='d', status=False, seller=request.user)

                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    @silk_profile(name='destroy products')
    def destroy(self, request, slug=None):
        """
                superuser can delete all objects
                but other user if is_seller=True and be seller object just can delete owner object
                :param request:
                :param slug:
                :return:
        """
        try:
            obj = productCacheDatabase(request, 'products', Product)
            product = obj.filter(slug=slug)
            product.delete()
            return response.SuccessResponse(message='Delete object').send()
        except CustomException as e:
            return response.ErrorResponse(message='Instance does not exist.', status=404).send()

    @action(detail=False, methods=['get'], name='items-search')
    def product_search(self, request):
        # http://localhost:8000/product/product_search/?search=mehran
        try:
            query = self.request.GET.get('search')
            objs = productCacheDatabase(request, 'products', Product)
            object_list = objs.filter(
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
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()


class CategoryViews(ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrOwnerCart,)
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
        try:
            obj = cacheCategoryOrFigur(request, 'category', Category)
            category = obj.filter(status=True)
            serializer = CategoryListSerializer(category, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    @silk_profile(name='detail category')
    def retrieve(self, request, slug=None):
        """
                detail category
                :param request:
                :param slug:
                :return:
        """
        try:
            obj = cacheCategoryOrFigur(request, 'category', Category)
            queryset = obj.filter(slug=slug)
            serializer = CategoryDetailSerializer(queryset, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    @staticmethod
    def create(request):
        try:
            serializer = CategoryInputSerializer(data=request.data)
            if serializer.is_valid() and request.user.is_superuser:
                serializer.save()
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    @silk_profile(name='update category')
    def update(self, request, slug=None):
        """
        update category
        :param request:
        :param slug:
        :return:
        """
        try:
            obj = cacheCategoryOrFigur(request, 'category', Category)
            category = obj.get(slug=slug)
            serializer = CategoryDetailSerializer(category, data=request.data)
            if serializer.is_valid() and request.user.is_superuser:
                serializer.save()
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    @silk_profile(name='destroy category')
    def destroy(self, request, slug=None):
        """
        delete object
        :param request:
        :param slug:
        :return:
        """
        try:
            obj = cacheCategoryOrFigur(request, 'category', Category)
            category = obj.get(slug=slug)
            category.delete()
            return response.SuccessResponse(message='Delete object').send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    # @silk_profile(name='product in category')
    @action(detail=True, methods=['get'], name='product-cat')
    def product_category(self, request, slug=None):
        """
        all products that in this category
        for example user click to mobile category and shows to user all products that be mobile category
        :param request:
        :param slug:
        :return:
        """
        try:
            obj_cat = cacheCategoryOrFigur(request, 'category', Category)
            obj_pro = productCacheDatabase(request, 'products', Product)
            queryset = obj_cat.get(slug=slug, status=True)
            products = obj_pro.filter(category=queryset)
            serializer = ProductSerializer(products, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()


class FigureViews(ViewSet):
    """
    figure fields for example:
    os:""
    color:""
    and ...
    """
    permission_classes = (IsSuperUserOrOwnerCart,)

    def list(self, request):
        try:
            obj = cacheCategoryOrFigur(request, 'figure', FigureField)
            serializer = FigureFieldSerializer(obj, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def retrieve(self, request, pk=None):
        try:
            obj = cacheCategoryOrFigur(request, 'figure', FigureField)
            queryset = obj.get(pk=pk)
            serializer = FigureFieldDetailSerializer(queryset)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def create(self, request):
        try:
            serializer = FigureFieldDetailSerializer(data=request.data)
            if serializer.is_valid() and request.user.is_superuser:
                serializer.save()
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def update(self, request, pk=None):
        try:
            obj = cacheCategoryOrFigur(request, 'figure', FigureField)
            figure = obj.get(pk=pk)
            serializer = FigureFieldDetailSerializer(figure, data=request.data)
            if serializer.is_valid() and request.user.is_superuser:
                serializer.save()
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def destroy(self, request, pk=None):
        """
        delete figure field
        :param request:
        :param pk:
        :return:
        """
        try:
            obj = cacheCategoryOrFigur(request, 'figure', FigureField)
            figure = obj.get(pk=pk)
            figure.delete()
            return response.SuccessResponse(message='Deleted object').send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()
