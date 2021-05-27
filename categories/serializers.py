from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)

from .models import (
    FigureField,
    Category
)


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
