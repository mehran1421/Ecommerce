# Generated by Django 3.2.3 on 2021-05-17 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_alter_cart_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=100, null=True, verbose_name='مجموع قیمت'),
        ),
    ]