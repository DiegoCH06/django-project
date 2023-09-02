from django.db import models
from rest_framework import serializers


# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
