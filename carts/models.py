from django.db import models
from users.models import User
from items.models import Product


class Cart(models.Model):
    """
    Store a cart belonging to a user.
    if user pay Cart ===> is_pay = True
    in payment app, it has been exported Factor that is_pay = True
    user can just cart objects that is_pay = False in carts app
    but in payment app show him all cart object is_pay = True
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    products = models.ManyToManyField(Product, through='CartItem', verbose_name='محصول')

    # sum of all line_item_total in CartItem
    # for example CartItem([line_item_total=100],[line_item_total=200] ===> subtotal = 300
    subtotal = models.DecimalField(default=0.00, null=True, blank=True, max_digits=100, decimal_places=2,
                                   verbose_name='مجموع قیمت')

    # count of CartItem
    # for example CartItem([line_item_total=100],[line_item_total=200] ===> total = 2
    total = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='تعداد')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='زمان اضاقه شدن')
    updated = models.DateTimeField(auto_now=True, verbose_name='زمان اپدیت')

    # for know that is pay cart or no
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
        """
        update subtotal in cart object
        each create or delete object in cartItem or product, call this functions
        :return:
        """
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = "%.2f" % subtotal
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, verbose_name='سبد خرید')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, verbose_name='محصول')

    # count of want product
    quantity = models.PositiveIntegerField(default=1)

    # sum of price product
    # for example product(price=100) and quantity is 4 ==> line_item_total = 400
    line_item_total = models.DecimalField(default=0.00, null=True, blank=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.title
