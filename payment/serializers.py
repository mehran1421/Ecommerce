from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from carts.models import Cart
from carts.serializers import CartItemListSerializers
from users.serializers import UserListSerializers, UserDetailSerializers
from items.serializers import ProductSerializer


class FactorListSerializers(ModelSerializer):
    detail = HyperlinkedIdentityField(view_name='pay:factor-detail')
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


class FactorDetailSerializers(ModelSerializer):
    user = UserDetailSerializers()

    class Meta:
        model = Cart
        fields = [
            'user',
            'subtotal',
            'total',
            'timestamp',
            'updated',
        ]
