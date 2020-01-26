from rest_framework import serializers
from .models import mqtt


class mqttSerializer(serializers.ModelSerializer):

    class Meta:
        model = mqtt
        fields = ('topic','payload','created_date' )
