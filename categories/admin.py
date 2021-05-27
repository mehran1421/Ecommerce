from django.contrib import admin
from .models import Category, FigureField


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'title', 'slug', 'position')
    list_filter = (['title'])
    search_fields = ('title', 'slug')
    list_editable = ['title', 'slug']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)

admin.site.register(FigureField)
