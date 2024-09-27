from django.db import models

class Gardens(models.Model):

    gardenID = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='gardens')
    name = models.CharField(max_length=100)
    private = models.BooleanField()
