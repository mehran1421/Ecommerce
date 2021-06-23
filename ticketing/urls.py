from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TicketViews,
    QuestionAnswerViews
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'ticket', TicketViews, basename='ticket')
router.register(r'answer', QuestionAnswerViews, basename='answer')

# The API URLs are now determined automatically by the router.
app_name = 'ticket'
urlpatterns = [
    path('', include(router.urls)),
]
