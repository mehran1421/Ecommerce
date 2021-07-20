# Generated by Django 2.2.23 on 2021-07-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=20, unique=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
