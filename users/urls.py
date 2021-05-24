from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViews

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViews, basename='user')

# The API URLs are now determined automatically by the router.
app_name = 'user'
urlpatterns = [
    path('', include(router.urls)),
]
