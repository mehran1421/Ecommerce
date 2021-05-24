from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PayViews

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'pay', PayViews, basename='payment')

# The API URLs are now determined automatically by the router.
app_name = 'pay'
urlpatterns = [
    path('request/', views.send_request, name='request'),
    path('verify/<int:pk>/', views.verify, name='verify'),
    path('', include(router.urls)),
]
