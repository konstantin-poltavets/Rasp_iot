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

class CalcManager(models.Manager): # Наш менеджер, который нам дает возможность менять поведение модели
    def get_query_set(self):
        result=super(CalcManager, self).get_query_set().extra(select={'price_liter': "price/liters"})
        return result


class gaz(models.Model):
    created_date = models.DateTimeField(default=timezone.now)

    GAZ_95 = 'GAZ_95'
    GAZ_98 = 'GAZ_98'
    LPG = 'LPG'
    GAZ_TYPES_CHOICES = ((GAZ_95, 'Gaz_95'), (GAZ_98, 'Gaz_98'), (LPG, 'LPG'),)

    fuel_type = models.CharField(max_length=6, blank=True,choices=GAZ_TYPES_CHOICES, default=LPG)

    liters = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    price_liter = CalcManager()
    objects = models.Manager()  # Стандартный менеджер