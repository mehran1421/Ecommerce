# Generated by Django 3.2.3 on 2021-05-14 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formfield',
            options={'verbose_name': 'فیلد محصول', 'verbose_name_plural': 'فیلد های محصول'},
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='موضوع'),
        ),
    ]
