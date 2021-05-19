from django.db import models
from my_user.models import User
from products_app.models import Product
from decimal import Decimal
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
            self.total += 1
        self.subtotal = "%.2f" % (subtotal)
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, verbose_name='سبد خرید')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.title


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if qty >= 1:
        price = instance.item.price
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()


post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)
