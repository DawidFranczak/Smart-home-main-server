from django.db import models
from django.contrib.auth.models import User
from devices.models import Device


# Create your models here.


class Temp(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=False)
    temp = models.CharField(max_length=10)
    humi = models.CharField(max_length=10, default="")

    def __str__(self):
        return str(self.device)
