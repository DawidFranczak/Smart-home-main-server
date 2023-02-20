from django.db import models
from devices.models import Device


class Light(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    light = models.BooleanField(default=False)

    def __str__(self):
        return str(self.device)
