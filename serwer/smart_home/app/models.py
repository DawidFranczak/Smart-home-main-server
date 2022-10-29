from email.policy import default
from sys import maxsize
from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import CharField
from sqlalchemy import false

# Create your models here.

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    port = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    fun = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)
    
    
class Temp(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    time = models.DateTimeField()
    temp = models.CharField(max_length=10)
    humi = models.CharField(max_length=10,default="")

    def __str__(self):
        return str(self.time)
    
class Sunblind(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.IntegerField()
    
class Aqua(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    color = models.CharField(max_length=100,default="")
    led_start = models.CharField(max_length=10,default="00:00:00")
    led_stop = models.CharField(max_length=10,default="00:00:00")
    fluo_start = models.CharField(max_length=10, default="00:00:00")
    fluo_stop = models.CharField(max_length=10, default="00:00:00")
    mode = models.BooleanField(default=False)
    led_mode = models.BooleanField(default=False)
    fluo_mode = models.BooleanField(default=False)

    
    def __str__(self):
        return str(self.mode)
    
    
class Stairs(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    steps = models.IntegerField(default = 200)
    brightness = models.IntegerField(default = 100)
    lightTime = models.IntegerField(default = 6)
    mode = models.BooleanField(default=False)
    
class Rfid(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    lamp = models.CharField(max_length=50,default="")
    
class Card(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,default="")
    uid = models.IntegerField(default=0)
    
class Button(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    lamp = models.CharField(max_length=50,default="")

class Light(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    light = models.BooleanField()
    