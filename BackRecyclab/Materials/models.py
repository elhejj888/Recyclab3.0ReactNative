from django.db import models
from authentication.models import Collector , User

class Material(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    etat = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deliveryAddress = models.CharField(max_length=255)
    quantity = models.IntegerField()
    transactionType = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MaterialImages(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Confirmation(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    collector = models.ForeignKey(Collector, on_delete=models.CASCADE)
    deliveryDate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)