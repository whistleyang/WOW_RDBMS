from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=20)

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    publish = models.CharField(max_length=32)
    pub_date = models.DateField()

class Employee(models.Model):  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    eid = models.CharField(max_length=20)  
    ename = models.CharField(max_length=100)  
    eemail = models.EmailField()  
    econtact = models.CharField(max_length=15)  
    class Meta:  
        db_table = "employee"  

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=32)
    lname = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    street = models.CharField(max_length=50)
    zipcode = models.DecimalField(max_digits=5,decimal_places=0)
    email = models.EmailField()
    phone = models.DecimalField(max_digits=11, decimal_places=0)
    cust_type = models.CharField(max_length=1)
