from django.db import models
from users.models import User
from items.models import Product
from django.db.models.signals import pre_save, post_save, post_delete


class Cart(models.Model):
    """
    Store a cart belonging to a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    products = models.ManyToManyField(Product, through='CartItem', verbose_name='محصول')
    subtotal = models.DecimalField(default=0.00, null=True, blank=True, max_digits=100, decimal_places=2,
                                   verbose_name='مجموع قیمت')
    total = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='تعداد')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='زمان اضاقه شدن')
    updated = models.DateTimeField(auto_now=True, verbose_name='زمان اپدیت')
    is_pay = models.BooleanField(default=False, verbose_name="آیا پرداخت شده")

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return str(self.user.get_full_name()) + " : " + str(self.user.username)

    def update_subtotal(self):
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = "%.2f" % (subtotal)
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, verbose_name='سبد خرید')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.title
