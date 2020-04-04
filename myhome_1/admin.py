from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import mqtt, Payment, gazoline, orbi_tmp, orbitrack
from api.models import Bucketlist

admin.site.register(mqtt)
admin.site.register(Payment)
admin.site.register(gazoline)
admin.site.register(Bucketlist)
admin.site.register(orbi_tmp)
admin.site.register(orbitrack)
#admin.site.register(Calc)
#admin.site.register(CalcManager1)