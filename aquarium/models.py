from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# class Device(models.Model):
#     user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     ip = models.CharField(max_length=100)
#     port = models.IntegerField()
#     created = models.DateTimeField(auto_now_add=True)
#     fun = models.CharField(max_length=100, default="")

#     def __str__(self):
#         return str(self.name)


# class Aquarium(models.Model):
#     device = models.OneToOneField(Device, on_delete=models.CASCADE)
#     color = models.CharField(max_length=100, default="r255g255b255")
#     led_start = models.CharField(max_length=10, default="00:00:00")
#     led_stop = models.CharField(max_length=10, default="00:00:00")
#     fluo_start = models.CharField(max_length=10, default="00:00:00")
#     fluo_stop = models.CharField(max_length=10, default="00:00:00")
#     mode = models.BooleanField(default=False)
#     led_mode = models.BooleanField(default=False)
#     fluo_mode = models.BooleanField(default=False)

#     def __str__(self):
#         return str(self.device)
