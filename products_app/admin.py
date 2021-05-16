from django.contrib import admin
from .models import Product, Category, FormField, Images

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(FormField)
admin.site.register(Images)

