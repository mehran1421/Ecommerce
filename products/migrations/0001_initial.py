# Generated by Django 3.2.3 on 2021-05-27 10:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images', verbose_name='عکس')),
            ],
            options={
                'verbose_name': 'عکس',
                'verbose_name_plural': 'عکس ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='تایتل')),
                ('slug', models.SlugField(blank=True, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='مشخصات محصول')),
                ('thumbnail', models.ImageField(upload_to='images', verbose_name='عکس')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ساخته ')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='قیمت')),
                ('status', models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')),
                ('choice', models.CharField(choices=[('d', 'درحال بررسی'), ('p', 'تغییرات صورت گرفته')], max_length=1, verbose_name='وضعیت')),
                ('category', models.ManyToManyField(related_name='product', to='categories.Category', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
                'ordering': ['-created'],
            },
        ),
    ]
