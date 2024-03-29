from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    username = models.CharField(max_length=300,default='username')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

class Department(models.Model):
    name = models.CharField(max_length=300)

class Resource(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    stock = models.IntegerField()
    department = models.ManyToManyField(Department)
    price = models.FloatField()

class EmployeeProfile(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    number = models.IntegerField()
    email = models.EmailField()
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)

class Vendor(models.Model):
    name = models.CharField(max_length=300)
    number = models.IntegerField()
    email = models.EmailField()

class Purchase(models.Model):
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    purchase_quantity = models.IntegerField()
    purchase_price = models.FloatField()
    purchase_from = models.ForeignKey(Vendor,on_delete=models.CASCADE)
        