from django.urls import path
from .views import CartListApi, CartListCreateApi,CartItemCreateApi,CartItemDeleteApi

app_name = 'cart'
urlpatterns = [
	path('all/', CartListApi.as_view(), name='list'),
	path('user/', CartListCreateApi.as_view(), name='list-user'),
	path('cart_item/user/', CartItemCreateApi.as_view(), name='list-create-cart-item'),
	path('cart_item/user/<int:pk>/',CartItemDeleteApi.as_view(),name='delete-cartItem'),
]
