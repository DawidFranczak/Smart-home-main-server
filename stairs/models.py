from django.db import models
from devices.models import Device


class Stair(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    steps = models.IntegerField(default=200)
    brightness = models.IntegerField(default=100)
    lightTime = models.IntegerField(default=6)
    mode = models.BooleanField(default=False)

    def __str__(self):
        return str(self.device)
