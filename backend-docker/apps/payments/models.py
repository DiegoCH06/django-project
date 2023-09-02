from django.db import models
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from apps.orders.models import Order


# Create your models here.
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField(null=False, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    orders = models.ManyToManyField(Order)


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = ('id', 'total', 'user', 'orders')
        extra_kwargs = {
                            'user': {
                                'required': False,
                            }
                        }
