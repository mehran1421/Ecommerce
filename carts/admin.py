from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'subtotal', 'total', 'timestamp',)
    list_filter = (['user', 'subtotal'])
    search_fields = ('user__first_name', 'user__last_name', 'subtotal', 'products')
    list_editable = ['subtotal', 'total']


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
