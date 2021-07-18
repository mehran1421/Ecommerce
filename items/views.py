from rest_framework.viewsets import ViewSet
from silk.profiling.profiler import silk_profile
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from extension.utils import productCacheDatabase, cacheDetailProduct, cacheCategoryOrFigur
from .permissions import (
    IsSuperUserOrIsSeller,
    IsSellerOrSuperUserObject,
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
        elif self.action in ['list', 'retrieve']:
            permission_classes = ()
        else:
            permission_classes = (IsSellerOrSuperUserObject,)

        return [permission() for permission in permission_classes]

    lookup_field = 'slug'

    @silk_profile(name='list products')
    def list(self, request):
        """
        for superuser return all object and
        for other user return Objects that status=True,choice='p'
        :param request:
        :return:
        """
        product = productCacheDatabase(request, 'products', Product)
        if not request.user.is_superuser:
            obj = product.filter(status=True, choice='p')
            product = obj
        serializer = ProductSerializer(product, context={'request': request}, many=True)
        return Response(serializer.data)

    @silk_profile(name='create products')
    def create(self, request):
        """
        create object and put choice='d',status=False,seller=request.user
        and superuser must ok object ====> status=True,choice='p' for shows site
        :param request:
        :return:
        """
        try:
            cat = Category.objects.first()

            serializer = InputProductSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(choice='d', status=False, seller=request.user, category=cat)
            else:
                print(serializer.errors)
                return Response({'status': 'Serializer information is not valid'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({"requirements field": 'no k'}, status=500)

    @silk_profile(name='detail products')
    def retrieve(self, request, slug=None):
        """
               superuser can see all object detail
               but other user just objects that status=True,choice='p'
               :param request:
               :param slug:
               :return:
        """
        if request.user.is_superuser:
            queryset = Product.objects.get(slug=slug)
        else:
            queryset = cacheDetailProduct(request, f'product_{slug}', slug, Product)

        serializer = ProductDetailSerializer(queryset, context={'request': request})
        return Response(serializer.data)

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
        obj = productCacheDatabase(request, 'products', Product)
        product = obj.filter(slug=slug)
        serializer = ProductDetailSerializer(product, data=request.data)
        if serializer.is_valid():
            if request.user.is_superuser:
                serializer.save()
            else:
                serializer.save(choice='d', status=False, seller=request.user)
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    @silk_profile(name='destroy products')
    def destroy(self, request, slug=None):
        """
                superuser can delete all objects
                but other user if is_seller=True and be seller object just can delete owner object
                :param request:
                :param slug:
                :return:
        """
        obj = productCacheDatabase(request, 'products', Product)
        product = obj.filter(slug=slug)
        product.delete()
        return Response({'status': 'ok'}, status=200)

    @action(detail=False, methods=['get'], name='items-search')
    def product_search(self, request):
        # http://localhost:8000/product/product_search/?search=mehran
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
        return Response(serializer.data)


class CategoryViews(ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrReadonly,)
        else:
            permission_classes = ()
        return [permission() for permission in permission_classes]

    lookup_field = 'slug'

    @silk_profile(name='list category')
    def list(self, request):
        """
        list all category
        :param request:
        :return:
        """
        obj = cacheCategoryOrFigur(request, 'category', Category)
        category = obj.filter(status=True)
        serializer = CategoryListSerializer(category, context={'request': request}, many=True)
        return Response(serializer.data)

    @silk_profile(name='detail category')
    def retrieve(self, request, slug=None):
        """
                detail category
                :param request:
                :param slug:
                :return:
        """
        obj = cacheCategoryOrFigur(request, 'category', Category)
        queryset = obj.filter(slug=slug)
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

    @silk_profile(name='update category')
    def update(self, request, slug=None):
        """
        update category
        :param request:
        :param slug:
        :return:
        """
        obj = cacheCategoryOrFigur(request, 'category', Category)
        category = obj.get(slug=slug)
        serializer = CategoryDetailSerializer(category, data=request.data)
        if serializer.is_valid() and request.user.is_superuser:
            serializer.save()
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    @silk_profile(name='destroy category')
    def destroy(self, request, slug=None):
        """
        delete object
        :param request:
        :param slug:
        :return:
        """
        obj = cacheCategoryOrFigur(request, 'category', Category)
        category = obj.get(slug=slug)
        if request.user.is_superuser:
            category.delete()
        return Response({'status': 'ok'}, status=200)

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
        objCat = cacheCategoryOrFigur(request, 'category', Category)
        objPro = productCacheDatabase(request, 'products', Product)
        queryset = objCat.get(slug=slug, status=True)
        products = objPro.filter(category=queryset)
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
        obj = cacheCategoryOrFigur(request, 'figure', FigureField)
        serializer = FigureFieldSerializer(obj, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = cacheCategoryOrFigur(request, 'figure', FigureField)
        queryset = obj.get(pk=pk)
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
        obj = cacheCategoryOrFigur(request, 'figure', FigureField)
        figure = obj.get(pk=pk)
        serializer = FigureFieldDetailSerializer(figure, data=request.data)
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
        obj = cacheCategoryOrFigur(request, 'figure', FigureField)
        figure = obj.get(pk=pk)
        if request.user.is_superuser:
            figure.delete()
        return Response({'status': 'ok'}, status=200)
