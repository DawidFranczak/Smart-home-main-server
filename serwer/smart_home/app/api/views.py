from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import *
from .serialized import *

@api_view(['GET'])
def test(request):
    test = ['test']
    return Response(test)

@api_view(['GET'])
def getAqua(request,pk):
    settings = Aqua.objects.get(sensor_id = pk)  
    serializer = AquaSerializer(settings, many=False)
    print(serializer)
    return Response(serializer.data)