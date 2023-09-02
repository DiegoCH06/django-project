from django.db import models
from rest_framework import serializers
from django.utils import timezone
from apps.users.models import User
from apps.orders.models import Order


# Create your models here.
class Shipment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    type = models.CharField(max_length=30, default="")
    orders = models.ManyToManyField(Order)


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'
