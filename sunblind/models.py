from django.db import models
from devices.models import Device


class Sunblind(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.device)
