# Generated by Django 3.2.3 on 2021-05-27 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='line_item_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
