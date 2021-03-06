from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone = models.IntegerField()
    deletedOn = models.DateField(default=None, null=True)

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    deletedOn = models.DateField(default=None, null=True)
    # converts category choices to readable names
    def __str__(self):
      return f'{self.name}'

class Product(models.Model):
    seller = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    dateAdded = models.DateField(default=None)
    deletedOn = models.DateField(default=None, null=True)

class PaymentType(models.Model):
    name = models.CharField(max_length=30)
    cardNum = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    deletedOn = models.DateField(default=None, null=True)

class Order(models.Model):
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    paymentType = models.ForeignKey(PaymentType, null=True, on_delete=models.CASCADE)
    deletedOn = models.DateField(default=None, null=True)

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    deletedOn = models.DateField(default=None, null=True)



