from django.db import models


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

    form_field = models.ManyToManyField(FigureField, default=None, blank=True,
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
