from django.db import models
from django.utils import timezone
from .utils import unique_slug_generator
from django.db.models.signals import pre_save


class FormField(models.Model):
    '''
    different fields for each category
    frontend developer use this to figure out what fields the user needs to fill
    '''
    type_product = models.JSONField(verbose_name='فیلد های این دسته بندی')

    class Meta:
        verbose_name = "فیلد محصول"
        verbose_name_plural = "فیلد های محصول"


class Category(models.Model):
    '''
    for Grouping product data
    '''
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name="زیردسته")
    title = models.CharField(max_length=200, unique=True, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(blank=True, verbose_name="موضوع")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    # each category has a form field
    # That's why I did this because the category may not have any fields
    # for example (کالای دیجیتال)
    form_field = models.OneToOneField(FormField, blank=True, null=True, on_delete=models.CASCADE, verbose_name='فیلدها')
    position = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['position']

    def __str__(self):
        return self.title


class Product(models.Model):
    '''
    product---------category
    samsung j7     کالای دیجیتال-موبایل
    '''
    title = models.CharField(max_length=200, verbose_name="تایتل")
    slug = models.SlugField(blank=True, verbose_name="عنوان")
    category = models.ManyToManyField(Category, related_name='product', verbose_name="دسته بندی")
    description = models.JSONField(verbose_name='مشخصات محصول')
    # The main photo of the product that is shown to the user
    thumbnail = models.ImageField(upload_to='images', blank=True, verbose_name="عکس")
    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان")
    created = models.DateTimeField(auto_now_add=True, verbose_name="ساخته ")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['-created']

    def __str__(self):
        return self.title

    def category_published(self):
        return self.category.filter(status=True)

    def category_to_string(self):
        caty = []
        for cat in self.category_published():
            caty.append(
                {
                    "name": "{0}".format(cat.title),
                    "slug": "{0}".format(cat.slug),
                    "fields": cat.form_field.type_product
                }
            )
        return caty


# signals for automatic fill slug field
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Product)


class Images(models.Model):
    '''
    images for each product that can to have many
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کدام محصول')
    image = models.ImageField(upload_to='images', verbose_name="عکس")

    class Meta:
        verbose_name = "عکس"
        verbose_name_plural = "عکس ها"


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کدام محصول')
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.product.title + ' : ' + str(self.price)

    class Meta:
        verbose_name = 'اطلاعات محصول'
        ordering = ['price']
