from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import CartItem
from decimal import Decimal


@receiver(pre_save, sender=CartItem)
def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if qty >= 1:
        price = instance.item.price
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total


@receiver([post_save, post_delete], sender=CartItem)
def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()
    cache.delete('cartItem-list')
