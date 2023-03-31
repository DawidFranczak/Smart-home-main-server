from rest_framework.serializers import ModelSerializer
from devices.models import Sensor


class SensorSerializer(ModelSerializer):
    class Meta:
        model = Sensor
        fields = ["ip", "port", "name"]
