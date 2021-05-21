from django.contrib import admin
from .models import Product, Category, FigureField, Images


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'category_to_string', 'publish', 'price', 'status',)
    list_filter = (['status', 'price'])
    search_fields = ('title', 'description')
    list_editable = ['status', 'price']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'title', 'slug', 'position',)
    list_filter = (['title'])
    search_fields = ('title', 'slug')
    list_editable = ['title', 'slug']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)

admin.site.register(FigureField)
admin.site.register(Images)
