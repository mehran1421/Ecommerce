from django.dispatch import receiver
from django.core.cache import cache
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


@receiver(post_delete, sender=CartItem)
def cart_item_pre_delete_receiver(sender, instance, *args, **kwargs):
    cache.delete('cartItem-list')
    if not instance.cart.is_pay:
        instance.cart.update_subtotal()


@receiver(post_save, sender=CartItem)
def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    cache.delete('cartItem-list')
    if not instance.cart.is_pay:
        instance.cart.update_subtotal()


@receiver(pre_delete, sender=Cart)
def cart_post_save_receiver(sender, instance, *args, **kwargs):
    cache.delete('cart-list')
    cache.delete('cartItem-list')


@receiver(post_save, sender=Cart)
def cart_pre_save_receiver(sender, instance, *args, **kwargs):
    cache.delete('cart-list')
