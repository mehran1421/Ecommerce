from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from .models import (
    Product,
    Category,
    FormField,
    Images,
    Variation
)


class FormFieldSerializer(ModelSerializer):
    class Meta:
        model = FormField
        fields = [
            'type_product',
        ]


class VariationSerializer(ModelSerializer):
    class Meta:
        model = Variation
        fields = [
            "id",
            "title",
            "price",
        ]


class CategorySerializer(ModelSerializer):
    form_field = FormFieldSerializer()
    product_category = HyperlinkedIdentityField(view_name='product:product_category', lookup_field='slug')

    class Meta:
        model = Category
        fields = [
            'title',
            'product_category',
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
    url = HyperlinkedIdentityField(view_name='product:detail', lookup_field='slug')

    class Meta:
        model = Product
        fields = [
            'url',
            'title',
            'thumbnail',
            'publish',
            'created',
        ]


class ProductDetailSerializer(ModelSerializer):
    category = CategorySerializer(many=True)
    images = SerializerMethodField()
    variation_set = VariationSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'category',
            'thumbnail',
            'images',
            'publish',
            'created',
            'variation_set'
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
