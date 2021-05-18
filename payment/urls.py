from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.send_request, name='request'),
    path('verify/<int:pk>/', views.verify, name='verify'),
]
