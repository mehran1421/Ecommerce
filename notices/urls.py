from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViews

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'notice', NoticeViews, basename='notice')

# The API URLs are now determined automatically by the router.
app_name = 'notice'
urlpatterns = [
    path('', include(router.urls)),
]
