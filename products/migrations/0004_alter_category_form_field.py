# Generated by Django 3.2.3 on 2021-05-25 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_category_form_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='form_field',
            field=models.ManyToManyField(blank=True, default=None, to='products.FigureField', verbose_name='فیلدها'),
        ),
    ]
