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
    created_date = models.DateField(default=timezone.now)

    GAZ_95 = 'GAZ_95'
    GAZ_98 = 'GAZ_98'
    LPG = 'LPG'
    GAZ_TYPES_CHOICES = ((GAZ_95, 'Gaz_95'), (GAZ_98, 'Gaz_98'), (LPG, 'LPG'),)

    fuel_type = models.CharField(max_length=6, blank=False,choices=GAZ_TYPES_CHOICES, default=LPG)
    liters = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    millage = models.PositiveIntegerField(blank=False, default=100000)

    BRSM = 'BRSM'
    KLO = 'KLO'
    LPG = 'LPG'
    WOG = 'WOG'
    STATION_TYPES_CHOICES = ((BRSM, 'BRSM'), (KLO, 'KLO'), (LPG, 'LPG'), (WOG, 'WOG'),)
    station_type = models.CharField(max_length=6, blank=True, choices=STATION_TYPES_CHOICES, default=BRSM)

    @property
    def cost(self):
        price_liter = self.price/self.liters
        return price_liter


    def __float__(self):
        return (self.price)



class CalcManager1(models.Manager): # Наш менеджер, который нам дает возможность менять поведение модели
    def get_query_set(self):
        result=super(CalcManager1, self).get_query_set().extra(select={'total': "first+second"})
        #то место где надо задавать алгоритм по которому вычисляется поле total
        return result

class Calc(models.Model):
    first = models.IntegerField(null=True)
    second = models.IntegerField(null=True)
    total = CalcManager1() # Созданный нами менеджер
    objects = models.Manager() # Стандартный менеджер

