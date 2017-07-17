# coding=utf-8
from django.db import models

# Create your models here.


class ServerView(models.Model):
    Address = models.CharField(max_length=50, primary_key=True)
    Name = models.CharField(max_length=50)
    Date = models.DateField()
    Disk = models.CharField(max_length=50)
    DiskUse = models.TextField()
    Mem = models.CharField(max_length=50)
    MemUse = models.TextField()
    RedisUse = models.TextField()