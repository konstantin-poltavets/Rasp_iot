from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Avg, Count, Sum

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



class gazoline(models.Model):
    created_date = models.DateField(default=timezone.now)

    Benzine = 'B'
    LPG = 'LPG'
    GAZ_TYPES_CHOICES = ((Benzine, 'B'), (LPG, 'LPG'),)
    fuel_type = models.CharField(max_length=7, blank=False,choices=GAZ_TYPES_CHOICES, default=LPG)

    liters = models.DecimalField(max_digits=7, decimal_places=2)
    price_liter = models.DecimalField(max_digits=7, decimal_places=2)
    price_after_disc = models.DecimalField(max_digits=7, decimal_places=2)
    millage = models.PositiveIntegerField(blank=False, default=120000)

    BRSM = 'BRSM'
    KLO = 'KLO'
    LPG = 'LPG'
    WOG = 'WOG'
    Other = 'Other'
    STATION_TYPES_CHOICES = ((BRSM, 'BRSM'), (KLO, 'KLO'), (LPG, 'LPG'), (WOG, 'WOG'), (Other, 'Other'))
    station = models.CharField(max_length=6, blank=True, choices=STATION_TYPES_CHOICES, default=BRSM)

    @property
    def price_before_disc(self):
        return self.price_liter * self.liters

    @property
    def disc(self):
        return self.price_liter * self.liters - self.price_after_disc

    class Meta:
        ordering = ["-created_date", "-id"]

    def __float__(self):
        return (self.price)

