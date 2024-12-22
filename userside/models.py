from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Product(models.Model):
    productname=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    price=models.IntegerField()
    image=models.ImageField(upload_to= 'images')
    def __str__(self):
        return self.productname


class CustomUser(AbstractUser):
     def __str__(self):
        return self.username


    