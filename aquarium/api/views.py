from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from devices.models import Sensor
from log.models import Ngrok

from .serialized import AquaSerializer, AquasSerializer


@api_view(["GET"])
def get_aqua(request, pk):
    """
    The function returns settings of the selected aquarium.

    endpoint: api/aquarium/<pk>

    """
    try:
        settings = request.user.sensor_set.get(pk=pk).aqua
        serializer = AquaSerializer(settings, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Sensor.DoesNotExist:
        return redirect("home")


@api_view(["POST"])
def get_aqua_all(request):
    """
    The function returns settings of the all aquariums.

    endpoint: api/aquarium/all
    """
    try:
        ngrok = request.POST.get("url")
        user = Ngrok.objects.get(ngrok=ngrok).user
        sensors = user.sensor_set.filter(fun="aqua")
        data = [AquasSerializer(sensor.aqua, many=False).data for sensor in sensors]
        return Response(data, status=status.HTTP_200_OK)

    except Ngrok.DoesNotExist:
        return redirect("home")


@api_view(["POST"])
# api/aquarium/update/
def update_aqua(request):
    """
    The function updated fluo and led mode of aquarium

    endpoint: api/aquarium/all
    """
    try:
        ngrok = request.data.get("url")
        user = Ngrok.objects.get(ngrok=ngrok).user
        for setting in request.data.get("settings"):
            if setting["response"]:
                aqua = user.sensor_set.get(ip=setting["ip"]).aqua
                aqua.fluo_mode = setting["fluo_mode"]
                aqua.led_mode = setting["led_mode"]
                aqua.save(update_fields=["fluo_mode", "led_mode"])

        return Response({}, status=status.HTTP_200_OK)
    except Ngrok.DoesNotExist:
        return redirect("home")
