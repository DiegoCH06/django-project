# Generated by Django 4.2.4 on 2023-08-28 04:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_paid_order_payments_order_products_order_total_and_more'),
        ('users', '0002_user_email_user_first_name_user_last_name_and_more'),
        ('shipments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='shipment',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]