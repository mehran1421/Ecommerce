from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import send_request, verify, Factors

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'factor', Factors, basename='factor')

# The API URLs are now determined automatically by the router.
app_name = 'pay'
urlpatterns = [
    path('request/', send_request, name='request'),
    path('verify/<int:pk>/', verify, name='verify'),
    path('', include(router.urls)),
]
