from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViews,
    FigureViews
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'category', CategoryViews, basename='category')
router.register(r'figure', FigureViews, basename='figure')

# The API URLs are now determined automatically by the router.
app_name = 'category'
urlpatterns = [
    path('', include(router.urls)),
]
