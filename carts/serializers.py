from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from .models import Cart, CartItem
from products.serializers import ProductSerializer


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


class CartItemDetailSerializers(ModelSerializer):
    # delete = HyperlinkedIdentityField(view_name='cart:delete-cartItem', lookup_field='pk')

    class Meta:
        model = CartItem
        fields = [
            'cart',
            # 'delete',
            'item',
            'quantity',
            'line_item_total',
        ]


class CartListSerializers(ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'user',
            'subtotal',
            'total',
            'timestamp',
            'updated',
        ]


class CartDetailSerializers(ModelSerializer):
    # products = ProductSerializer(many=True)
    # cart_item = CartItemListSerializers(source='cartitem_set', many=True)

    # first add MERCHANT in payment app
    # must connect to internet
    # pay = HyperlinkedIdentityField(view_name='pay:request')

    class Meta:
        model = Cart
        fields = [
            'user',
            # 'cart_item',
            # 'pay',
            'products',
            'subtotal',
            'total',
            'timestamp',
            'updated',
        ]
