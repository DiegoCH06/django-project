# Generated by Django 4.2.4 on 2023-08-31 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_payments'),
        ('payments', '0002_payment_total_payment_user_alter_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='orders',
            field=models.ManyToManyField(to='orders.order'),
        ),
    ]