from django.db import models
from devices.models import Device
# Create your models here.


class Aqua(models.Model):
    aquarium = models.OneToOneField(Device, on_delete=models.CASCADE)
    color = models.CharField(max_length=100, default="r255g255b255")
    led_start = models.CharField(max_length=10, default="00:00:00")
    led_stop = models.CharField(max_length=10, default="00:00:00")
    fluo_start = models.CharField(max_length=10, default="00:00:00")
    fluo_stop = models.CharField(max_length=10, default="00:00:00")
    mode = models.BooleanField(default=False)
    led_mode = models.BooleanField(default=False)
    fluo_mode = models.BooleanField(default=False)

    def __str__(self):
        return self.device
