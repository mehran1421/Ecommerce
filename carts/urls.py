from django.urls import path
from .views import CartListApi,CartListCreateApi

app_name = 'cart'
urlpatterns = [
    path('all/',CartListApi.as_view(),name='list'),
    path('user/',CartListCreateApi.as_view(),name='list-user'),
]
