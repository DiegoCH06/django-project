# Generated by Django 4.2.4 on 2023-08-31 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_count_product_name_product_prince_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='prince',
            new_name='price',
        ),
    ]