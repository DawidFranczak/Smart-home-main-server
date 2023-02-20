from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Device(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    port = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    fun = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.name)
