from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from .models import Cart, CartItem
from products_app.serializers import ProductDetailSerializer


class CartItemSerializers(ModelSerializer):
    item = ProductDetailSerializer(many=True)

    class Meta:
        model = Cart
        fields = [
            'cart',
            'item',
            'quantity',
            'line_item_total',
        ]


class CartSerializers(ModelSerializer):
    products = ProductDetailSerializer(many=True)

    class Meta:
        model = Cart
        fields = [
            'user',
            'products',
            'subtotal',
            'total',
            'timestamp',
            'updated',
        ]
