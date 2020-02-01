from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import mqtt, Payment, gaz
from api.models import Bucketlist

admin.site.register(mqtt)
admin.site.register(Payment)
admin.site.register(gaz)
admin.site.register(Bucketlist)