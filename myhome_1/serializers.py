from django.db.models import QuerySet, Sum
from rest_framework import serializers
from .models import mqtt, gazoline


class mqttSerializer(serializers.ModelSerializer):

    class Meta:
        model = mqtt
        fields = ('topic','payload','created_date' )


class gazSerializer(serializers.ModelSerializer):


    class Meta:
        model = gazoline
        fields = ('created_date','liters','millage','fuel_type')

