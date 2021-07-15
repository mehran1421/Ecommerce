from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    is_seller = models.BooleanField(default=False, verbose_name='آیا کاربر فروشنده است')
