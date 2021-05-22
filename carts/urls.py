from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import ProductViews, CategoryViews

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'product', ProductViews, basename='product')


# The API URLs are now determined automatically by the router.
app_name = 'carts'
urlpatterns = [
    path('', include(router.urls)),
]
