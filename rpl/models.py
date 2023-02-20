from django.db import models
from devices.models import Device


class Rfid(models.Model):
    sensor = models.OneToOneField(Device, on_delete=models.CASCADE)
    lamp = models.CharField(max_length=50, default="")

    def __str__(self):
        return str(self.sensor)


class Card(models.Model):
    sensor = models.ForeignKey(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="")
    uid = models.IntegerField(default=0)

    def __str__(self):
        return str(self.rfid)


class Button(models.Model):
    sensor = models.OneToOneField(Device, on_delete=models.CASCADE)
    lamp = models.CharField(max_length=50, default="")

    def __str__(self):
        return str(self.sensor)
