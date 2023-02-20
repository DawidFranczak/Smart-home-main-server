from rest_framework.serializers import ModelSerializer
from stairs.models import Stairs


class StairsSerializer(ModelSerializer):
    class Meta:
        model = Stairs
        fields = '__all__'
