from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViews, CategoryViews

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'product', ProductViews, basename='product')
router.register(r'category', CategoryViews, basename='category')

# The API URLs are now determined automatically by the router.
app_name = 'product'
urlpatterns = [
    path('', include(router.urls)),
]
