from django.db import models

# Create your models here.

class SalesUser(models.Model):
    userid = models.CharField(max_length=50,primary_key=True)
    firstname = models.CharField(max_length=50,default="")
    lastname = models.CharField(max_length=50,default="")
    email = models.CharField(max_length=50,default="")
    username = models.CharField(max_length=50,default="")