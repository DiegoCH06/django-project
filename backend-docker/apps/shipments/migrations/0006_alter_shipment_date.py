# Generated by Django 4.2.4 on 2023-08-31 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0005_rename_order_shipment_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
