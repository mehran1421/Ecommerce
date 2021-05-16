from django.db import models
from account.models import User
from products_app.models import Product


class Cart(models.Model):
    """
    Store a cart belonging to a user.
    """
    user = models.ForeignKey(User, verbose_name='کاربر')
    products = models.ManyToManyField(Product, blank=True, verbose_name='محصول')
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2, verbose_name='مجموع قیمت')
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2, verbose_name='قیمت')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='زمان اضاقه شدن')
    updated = models.DateTimeField(auto_now=True, verbose_name='زمان اپدیت')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

    def __str__(self):
        return str(self.id)
