from rest_framework.serializers import ModelSerializer
from app.models import *

class AquaSerializer(ModelSerializer):
    class Meta:
        model = Aqua
        fields = '__all__'