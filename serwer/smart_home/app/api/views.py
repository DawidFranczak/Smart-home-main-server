from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import *
from app.mod import data_for_chart
from .serialized import *
from datetime import datetime, timedelta
from django.http import JsonResponse



@api_view(['GET'])
def test(request):
    test = ['test']
    return Response(test)

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