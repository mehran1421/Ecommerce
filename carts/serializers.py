from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField
from .models import Cart
from products_app.serializers import ProductDetailSerializer


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
