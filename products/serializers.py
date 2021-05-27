from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from .models import (
    Product,
    Images,
)
from categories.serializers import CategoryListSerializer
from users.serializers import UserListSerializers


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
