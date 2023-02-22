from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serialized import AquaSerializer
from devices.models import Sensor


@api_view(['GET'])
def getAqua(request, pk):
    settings = request.user.sensor_set.get(pk=pk).aqua
    settings = Sensor.objects.get(pk=pk).aqua
    serializer = AquaSerializer(settings, many=False)
    return Response(serializer.data)
