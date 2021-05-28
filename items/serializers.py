from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from .models import (
    Product,
    Images,
    Category,
    FigureField
)
from users.serializers import UserListSerializers


class FigureFieldSerializer(ModelSerializer):
    """
    Property product
    """

    class Meta:
        model = FigureField
        fields = [
            'type_product',
        ]


class CategoryInputSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'title',
            'slug',
            'status',
            'position',
        ]


class CategoryListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='product:category-detail', lookup_field='slug')

    class Meta:
        model = Category
        fields = [
            'url',
            'title',
            'slug',
        ]


class CategoryDetailSerializer(ModelSerializer):
    """
    list category
    have a link for list product with selected category(product_category)
    """
    forms_field = SerializerMethodField()
    product_category = HyperlinkedIdentityField(view_name='product:category-product-category', lookup_field='slug')

    class Meta:
        model = Category
        fields = [
            'title',
            'slug',
            'product_category',
            'status',
            'forms_field',
            'position',
        ]

    def get_forms_field(self, obj):
        form_list = []
        for i in obj.form_field.all():
            form_list.append(i.type_product)
        return form_list


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'image',
        ]


class ProductSerializer(ModelSerializer):
    """
    list product
    have a link for get detail product with (url)
    """
    url = HyperlinkedIdentityField(view_name='product:product-detail', lookup_field='slug')

    class Meta:
        model = Product
        fields = [
            'url',
            'slug',
            'title',
            'thumbnail',
            'price',
            'persian_publish'
        ]


class ProductDetailSerializer(ModelSerializer):
    """
    product detail any things
    """
    category = CategoryListSerializer(many=True)
    images = SerializerMethodField()
    seller = UserListSerializers()

    class Meta:
        model = Product
        fields = [
            'title',
            'slug',
            'seller',
            'description',
            'category',
            'thumbnail',
            'images',
            'persian_publish',
            'price',
            'status',
            'choice',
        ]

    def get_images(self, obj):
        image = {}
        count = 0
        for i in obj.images_set.all():
            count += 1
            image.update({
                "{0}".format(count): i.image.url
            })
        return image


class InputProductSerializers(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'category',
            'description',
            'seller',
            'thumbnail',
            'price',
        ]
