from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect


from .serialized import AquaSerializer, AquasSerializer
from devices.models import Sensor
from log.models import Ngrok


@api_view(['GET'])
def getAqua(request, pk):
    try:
        settings = request.user.sensor_set.get(pk=pk).aqua
        settings = Sensor.objects.get(pk=pk).aqua
        serializer = AquaSerializer(settings, many=False)
        return Response(serializer.data)
    except:
        return redirect('home')


@api_view(['POST'])
# api/aquarium/all
def getAquaAll(request):
    try:
        ngrok = request.POST.get('url')
        user = Ngrok.objects.get(ngrok=ngrok).user
        sensors = user.sensor_set.filter(fun='aqua')
        data = [AquasSerializer(
            sensor.aqua, many=False).data for sensor in sensors]
        return Response(data)
    except:
        return redirect('home')


@api_view(['POST'])
# api/aquarium/update/
def updateAqua(request):
    try:
        ngrok = request.data.get('url')
        user = Ngrok.objects.get(ngrok=ngrok).user
        for setting in request.data.get('settings'):
            if setting['response']:  # aquarium communications succesfully if True
                aqua = user.sensor_set.get(ip=setting['ip']).aqua
                aqua.fluo_mode = setting['fluo_mode']
                aqua.led_mode = setting['led_mode']
                aqua.save()

        return Response({'status': 'ok'})
    except:
        return redirect('home')
