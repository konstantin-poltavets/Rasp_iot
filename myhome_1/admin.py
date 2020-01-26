from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import mqtt, Payment

admin.site.register(mqtt)
admin.site.register(Payment)