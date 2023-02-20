from rest_framework.serializers import ModelSerializer
from devices.models import Stairs


class AquaSerializer(ModelSerializer):
    class Meta:
        model = Stairs
        exclude = ('id',)
