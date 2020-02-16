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


    def agregates(self, start_date, end_date):
        cont = []
        start_date_final = str(start_date)+ '-01-01'
        end_date_final = str(end_date)+ '-12-31'

        for y in range(start_date, end_date+1, 1):
            start_date = str(y) + '-01-01'

            end_date = str(y) + '-12-31'
            query = self.objects.all().filter(created_date__range=(start_date, end_date))

            milles_start = query.values("millage")[0]["millage"]
            milles_end = query.values("millage")[6]["millage"]
            milles = milles_end - milles_start

            print("milles   ",milles)

            #query_Avg = query.aggregate(Avg('price_liter'))["price_liter__avg"]
            query_Count = query.aggregate(Count('created_date'))["created_date__count"]
            query_Sum = query.aggregate(Sum('price_after_disc'))["price_after_disc__sum"]
            query_Liters = query.aggregate(Sum('liters'))["liters__sum"]
            query_Avg = query_Sum/query_Liters

            agr = {'start_date': start_date_final, 'end_date': end_date, 'query_Avg': query_Avg,
                   'query_Count': query_Count, 'query_Sum': query_Sum, 'query_Liters': query_Liters,
                   'milles': milles}

            cont.append(agr)

            #summary

        query = self.objects.all().filter(created_date__range=(start_date_final, end_date))
        query_Count = query.aggregate(Count('created_date'))["created_date__count"]
        query_Sum = query.aggregate(Sum('price_after_disc'))["price_after_disc__sum"]
        query_Liters = query.aggregate(Sum('liters'))["liters__sum"]
        query_Avg = query_Sum/query_Liters
        milles = 1000
        agr = {'start_date':start_date_final,'end_date':end_date, 'query_Avg':query_Avg,
               'query_Count':query_Count, 'query_Sum':query_Sum, 'query_Liters':query_Liters,
               'milles':milles}
        cont.append(agr)

        return cont







