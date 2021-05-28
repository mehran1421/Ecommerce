from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from .models import Cart, CartItem
from users.serializers import UserListSerializers
from items.serializers import ProductSerializer, ProductDetailSerializer


class CartItemInputSerializers(ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'cart',
            'item',
            'quantity',
        ]


class CartInputSerializers(ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'user',
            'items',
        ]


class CartItemListSerializers(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='carts:cart-item-detail')
    item = ProductSerializer()

    class Meta:
        model = CartItem
        fields = [
            'url',
            'cart',
            'item',
            'quantity',
            'line_item_total',
        ]


class CartListSerializers(ModelSerializer):
    detail = HyperlinkedIdentityField(view_name='carts:cart-detail')
    user = UserListSerializers()

    class Meta:
        model = Cart
        fields = [
            'detail',
            'user',
            'subtotal',
            'total',
            'timestamp',
            'updated',
        ]


class CartItemDetailSerializers(ModelSerializer):
    item = ProductDetailSerializer()
    cart = CartListSerializers()

    class Meta:
        model = CartItem
        fields = [
            'cart',
            'item',
            'quantity',
            'line_item_total',
        ]


class CartDetailSerializers(ModelSerializer):
    products = ProductSerializer(many=True)
    cart_item = CartItemListSerializers(source='cartitem_set', many=True)
    user = UserListSerializers()

    # first add MERCHANT in payment app
    # must connect to internet
    # pay = HyperlinkedIdentityField(view_name='pay:request')

    class Meta:
        model = Cart
        fields = [
            'user',
            'cart_item',
            # 'pay',
            'items',
            'subtotal',
            'total',
            'timestamp',
            'updated',
        ]
