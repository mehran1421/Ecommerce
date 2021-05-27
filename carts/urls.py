from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViews, CartViews

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'cartItem', CartItemViews, basename='cart-item')
router.register(r'cart', CartViews, basename='cart')

# The API URLs are now determined automatically by the router.
app_name = 'carts'
urlpatterns = [
    path('', include(router.urls)),
]
