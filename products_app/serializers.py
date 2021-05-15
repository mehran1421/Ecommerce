from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from .models import Product, Category, FormField


class FormFieldSerializer(ModelSerializer):
    class Meta:
        model = FormField
        fields = [
            'type_product',
        ]


class CategorySerializer(ModelSerializer):
    form_field = FormFieldSerializer()
    product_category = HyperlinkedIdentityField(view_name='product:product_category',lookup_field='slug')

    class Meta:
        model = Category
        fields = [
            'title',
            'product_category',
            'status',
            'form_field',
            'position',
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

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'category',
            'thumbnail',
            'publish',
            'created',
        ]
