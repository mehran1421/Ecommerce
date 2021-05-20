from django.urls import path
from .views import (
    ProductList,
    CategoryList,
    ProductDetail,
    ProductCategory
)

app_name = 'product'
urlpatterns = [
    path('list/', ProductList.as_view(), name='list'),
    path('list/<slug:slug>/', ProductDetail.as_view(), name='detail'),
    path('category/', CategoryList.as_view(), name='category'),
    path('category/<slug:slug>/', ProductCategory.as_view(), name='product_category'),
]
