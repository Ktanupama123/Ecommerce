from django.db import models
from django.conf import settings
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

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference the custom user model
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user.username} - {self.product.productname}'

