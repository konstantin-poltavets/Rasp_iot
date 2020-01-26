from django.contrib import admin
from .models import Modules, Boards, Mqtt, Mqttypes

admin.site.register(Modules)
admin.site.register(Boards)
admin.site.register(Mqtt)
admin.site.register(Mqttypes)