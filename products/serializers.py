from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from .models import (
    Product,
    Category,
    FigureField,
    Images,
)


class FigureFieldSerializer(ModelSerializer):
    class Meta:
        model = FigureField
        fields = [
            'type_product',
        ]


class CategorySerializer(ModelSerializer):
    form_field = FigureFieldSerializer(many=True)

    # product_category = HyperlinkedIdentityField(view_name='product:product_category', lookup_field='slug')

    class Meta:
        model = Category
        fields = [
            'title',
            'slug',
            # 'product_category',
            'status',
            'form_field',
            'position',
        ]


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'image',
        ]


class ProductSerializer(ModelSerializer):
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
    category = CategorySerializer(many=True)
    images = SerializerMethodField()

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
