from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from users.models import User
from extension.utils import jalaly_converter


class FigureField(models.Model):
    """
    different fields for each category
    frontend developer use this to figure out what fields the user needs to fill
    """
    type_product = models.CharField(max_length=200, verbose_name='فیلد های این دسته بندی')

    class Meta:
        verbose_name = "فیلد محصول"
        verbose_name_plural = "فیلد های محصول"

    def __str__(self):
        return self.type_product


class Category(models.Model):
    """
     for Grouping product data
    """
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name="زیردسته")
    title = models.CharField(max_length=200, unique=True, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(blank=True, verbose_name="موضوع")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    '''
    each category has a form field
    That's why I did this because the category may not have any fields
    for example (کالای دیجیتال)
    '''

    form_field = models.ManyToManyField(FigureField, blank=True, null=True,
                                        verbose_name='فیلدها')
    position = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['position']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title


class Product(models.Model):
    """
    product---------category
    samsung j7     کالای دیجیتال-موبایل
    """
    Status_Choise = (
        ('d', 'درحال بررسی'),
        ('p', 'تغییرات صورت گرفته'),
    )

    title = models.CharField(max_length=200, verbose_name="تایتل")
    slug = models.SlugField(blank=True, verbose_name="عنوان")
    category = models.ManyToManyField(Category, related_name='product', verbose_name="دسته بندی")
    description = models.TextField(verbose_name='مشخصات محصول')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='فروشنده')
    # The main photo of the product that is shown to the user
    thumbnail = models.ImageField(upload_to='images', null=True, blank=True, verbose_name="عکس")
    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان")
    created = models.DateTimeField(auto_now_add=True, verbose_name="ساخته ")
    price = models.DecimalField(decimal_places=2, default=00.00, max_digits=20, verbose_name='قیمت')
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    choice = models.CharField(max_length=1, choices=Status_Choise, verbose_name="وضعیت")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['-created']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def category_published(self):
        return self.category.filter(status=True)

    def category_to_string(self):
        return ", ".join([cat.title for cat in self.category_published()])

    category_to_string.short_description = "زیردسته"

    def thumbnail_tag(self):
        return format_html("<img width=100 src='{}'>".format(self.thumbnail.url))

    thumbnail_tag.short_description = "عکس"

    def persian_publish(self):
        return jalaly_converter(self.publish)

    persian_publish.short_description = "تاریخ"


class Images(models.Model):
    """
     images for each product that can to have many
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کدام محصول')
    image = models.ImageField(upload_to='images', verbose_name="عکس")

    class Meta:
        verbose_name = "عکس"
        verbose_name_plural = "عکس ها"
        indexes = [
            models.Index(fields=['product']),
        ]
