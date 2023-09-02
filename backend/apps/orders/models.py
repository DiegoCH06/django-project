from django.db import models
from rest_framework import serializers
from apps.products.models import Product
from django.contrib.auth.models import User


# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField(null=False, default=0)
    paid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('products', 'id', 'paid', 'total')
        extra_kwargs = {
            'id': {
                'required': False
            }
        }
