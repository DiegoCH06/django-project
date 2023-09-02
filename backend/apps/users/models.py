from django.db import models
from rest_framework import serializers


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField(unique=True, default="")
    password= models.CharField(max_length=100, default="")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
