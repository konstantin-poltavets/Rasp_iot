from django.conf import settings
from django.db import models
from django.utils import timezone



class mqtt(models.Model):
    topic = models.CharField(max_length=200)
    payload = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.topic


    #def __str__(self):
     #   return self.payload

class Payment(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=4)
    datetime = models.DateTimeField()
