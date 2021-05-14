from django.db import models
from django.utils import timezone
from .utils import unique_slug_generator
from django.db.models.signals import pre_save


class FormField(models.Model):
    type_product = models.JSONField(verbose_name='فیلد های این دسته بندی')

    class Meta:
        verbose_name = "فیلد محصول"
        verbose_name_plural = "فیلد های محصول"


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(blank=True, verbose_name="موضوع")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    form_field = models.OneToOneField(FormField,default=1,on_delete=models.CASCADE,verbose_name='فیلدها')
    position = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['position']

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="تایتل")
    slug = models.SlugField(blank=True, verbose_name="عنوان")
    category = models.ManyToManyField(Category, verbose_name="دسته بندی")
    description = models.JSONField(verbose_name='مشخصات محصول')
    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان")
    created = models.DateTimeField(auto_now_add=True, verbose_name="ساخته ")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"
        ordering = ['-created']

    def __str__(self):
        return self.title


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Product)
pre_save.connect(pre_save_receiver, sender=Category)

