from django.dispatch import receiver
from django.core.cache import cache, caches
from decimal import Decimal
from .models import (
    CartItem,
    Cart
)
from django.db.models.signals import (
    pre_save,
    pre_delete,
    post_save,
    post_delete
)


@receiver(pre_save, sender=CartItem)
def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if qty >= 1 and not instance.cart.is_pay:
        price = instance.item.price
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total


@receiver(pre_delete, sender=CartItem)
def cart_item_pre_delete_receiver(sender, instance, *args, **kwargs):
    caches['cartItems'].delete('cartItem-list')
    price_cart_item = instance.line_item_total
    instance.cart.subtotal -= price_cart_item
    instance.cart.save()


@receiver(post_save, sender=CartItem)
def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    caches['cartItems'].delete('cartItem-list')
    if not instance.cart.is_pay:
        instance.cart.update_subtotal()


@receiver(pre_delete, sender=Cart)
def cart_post_save_receiver(sender, instance, *args, **kwargs):
    user = instance.user
    cache.delete(f'cart-{user.email}')
    caches['cartItems'].delete('cartItem-list')


@receiver(post_save, sender=Cart)
def cart_pre_save_receiver(sender, instance, *args, **kwargs):
    user = instance.user
    cache.delete(f'cart-{user.email}')