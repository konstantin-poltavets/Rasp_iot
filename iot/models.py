from django.utils import timezone
from django.db import models


class Modules(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    photos = models.ImageField(upload_to='modules', blank=True, default='modules/missing.png')

    TEMPERATURE = 'TEMP'
    HUMIDITY = 'HUM'
    IR_RECEIVER = 'IR_R'
    IR_TRANSMITTER = 'IR_T'
    ALTITUDE = 'ALT'

    SENSORS_TYPES_CHOICES = ((TEMPERATURE, 'Temperature'), (HUMIDITY, 'Humidity'), (IR_RECEIVER, 'IR_Receiver')
                        , (IR_TRANSMITTER, 'IR_Transmitter'), (ALTITUDE, 'Altitude'),)

    type1 = models.CharField(max_length=6, blank=True,choices=SENSORS_TYPES_CHOICES, default=TEMPERATURE)
    type2 = models.CharField(max_length=6, blank=True,choices=SENSORS_TYPES_CHOICES, default='')
    type3 = models.CharField(max_length=6, blank=True,choices=SENSORS_TYPES_CHOICES, default='')
    type4 = models.CharField(max_length=6, blank=True,choices=SENSORS_TYPES_CHOICES, default='')






    def __str__(self):
        return self.name




class Boards(models.Model):
    LEAVING_ROOM = 'LR'
    KITCHEN = 'KN'
    CORRIDOR = 'KR'
    BEDROOM = 'BR'
    RESTROOM = 'RR'
    LOCATION_CHOICES =((LEAVING_ROOM, 'Leavingroom'),(KITCHEN, 'Kitchen'),(CORRIDOR, 'Corridor')
                       ,(BEDROOM, 'Bedroom'),(RESTROOM, 'Restroom'),)


    location = models.CharField(max_length=2, choices= LOCATION_CHOICES, default = LEAVING_ROOM )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(protocol='IPv4', default='0.0.0.0')
    topic_publish = models.CharField(max_length=50, blank=True)
    topic_subscribe = models.CharField(max_length=50, blank=True)
    sensor1 = models.ForeignKey(Modules, default=2, on_delete=models.DO_NOTHING, related_name='sensor1')
    sensor2 = models.ForeignKey(Modules, default=2, on_delete=models.DO_NOTHING, related_name='sensor2')
    sensor3 = models.ForeignKey(Modules, default=2, on_delete=models.DO_NOTHING, related_name='sensor3')
    sensor4 = models.ForeignKey(Modules, default=2, on_delete=models.DO_NOTHING, related_name='sensor4')
    processor = models.ForeignKey(Modules, default=2, on_delete=models.DO_NOTHING, related_name='processor')
    photos = models.ImageField(upload_to='modules', blank=True, default='modules/missing.png')
    scetch = models.FileField(upload_to='uploads/', blank = True)
    def __str__(self):
        return self.name


class Mqttypes(models.Model):
    SUBSCRIBE = 'S'
    PUBLISH = 'P'
    TYPE_CHOICES =((SUBSCRIBE, 'subscribe'),(PUBLISH, 'publish'),)

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=2, choices= TYPE_CHOICES, default = SUBSCRIBE )
    topic = models.CharField(max_length=200)

    def __str__(self):
        return self.topic


class Mqtt(models.Model):

    created_date = models.DateTimeField(default=timezone.now)
    topic = models.ForeignKey(Mqttypes, default='', on_delete=models.DO_NOTHING)
    payload = models.TextField()


    def __str__(self):
        return str(self.created_date)