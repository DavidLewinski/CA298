from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class APIUser(AbstractUser):
    pass

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(null = False, max_length=30)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    image = models.FileField(upload_to='products')

class Basket(models.Model):
    id = models.IntegerField(primary_key=True)
    UserID = models.ForeignKey(APIUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class BasketItem(models.Model):
    id = models.IntegerField(primary_key=True)
    BasketID = models.ForeignKey(Basket, on_delete=models.CASCADE)
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=1)

    def Price(self):
        return self.ProductID.price * self.Quantity

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    BasketID = models.ForeignKey(Basket, on_delete=models.CASCADE)
    UserID = models.ForeignKey(APIUser, on_delete=models.CASCADE)
    DateTimeOrdered = models.DateTimeField(auto_now_add=True)
    TotalPrice = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    ShippingCountry = models.TextField(default="")
    ShippingAddress1 = models.TextField(default="")
    ShippingAddress2 = models.TextField(default="")
    ShippingAddressZip = models.TextField(default="")