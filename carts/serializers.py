from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from .models import Cart, CartItem
from products_app.serializers import ProductSerializer


class CartItemSerializers(ModelSerializer):
	delete = HyperlinkedIdentityField(view_name='cart:delete-cartItem', lookup_field='pk')

	class Meta:
		model = CartItem
		fields = [
			'cart',
			'delete',
			'item',
			'quantity',
			'line_item_total',
		]


class CartSerializers(ModelSerializer):
	products = ProductSerializer(many=True)

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
