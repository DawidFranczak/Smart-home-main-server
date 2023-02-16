from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import Aqua, Stairs
from .serialized import AquaSerializer, StairsSerializer


@api_view(['GET'])
def getAqua(request,pk):
    settings = Aqua.objects.get(sensor_id = pk)  
    serializer = AquaSerializer(settings, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getStairs(request,pk):
    settings = Stairs.objects.get(sensor_id = pk)
    serializer = StairsSerializer(settings, many=False)
    return Response(serializer.data)