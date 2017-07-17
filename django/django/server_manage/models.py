from django.db import models

# Create your models here.
class ServerList(models.Model):
    ServerId = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    CreateTime = models.DateTimeField()

class User(models.Model):
    username = models.CharField(max_length=6)
    password = models.CharField(max_length=15)





