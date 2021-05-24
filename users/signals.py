from django.core.cache import cache
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save

User = get_user_model()


@receiver([post_delete, post_save], sender=User)
def pre_delete_receiver_user(sender, instance, *args, **kwargs):
    cache.delete('user-list')
