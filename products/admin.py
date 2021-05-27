from django.contrib import admin
from .models import Product, Images


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'category_to_string', 'persian_publish', 'price', 'status',)
    list_filter = (['status', 'price'])
    search_fields = ('title', 'description')
    list_editable = ['status', 'price']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Product, ProductAdmin)

admin.site.register(Images)
