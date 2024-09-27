from django.db import models

class Users(models.Model):

    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)