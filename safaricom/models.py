from django.db import models

# Create your models here.
class Payment(models.Model):
    first_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    amount = models.IntegerField()

    