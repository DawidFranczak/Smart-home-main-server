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
    This function either returns the aquarium settings or redirects the user
    to the homepage if they are not logged in

    endpotnt: api/aquarium/<int:pk>
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
    This function either returns the all aquariums settings or redirects the user
    to the homepage if they are not logged in

    endpotnt: api/aquarium/all
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
    This function updated settings.
    Request come from client sever.
    Request should be nested dictionary for each aquarium
    like below
    {
        "settings":[
                {
                "success": True,
                "fluo_mode": fluo_mode,
                "led_mode": led_mode,
                "ip": ip,
                },
                {
                "success": True,
                "fluo_mode": fluo_mode,
                "led_mode": led_mode,
                "ip": ip,
                }
                ...
            ]

    }

    endpotnt: api/aquarium/all
    """
    try:
        ngrok = request.data.get("url")
        user = Ngrok.objects.get(ngrok=ngrok).user
        for setting in request.data.get("settings"):
            if setting["response"]:
                aqua = user.sensor_set.get(ip=setting["ip"]).aqua
                aqua.fluo_mode = setting["fluo_mode"]
                aqua.led_mode = setting["led_mode"]
                aqua.save()

        return Response({}, status=status.HTTP_200_OK)
    except Ngrok.DoesNotExist:
        return redirect("home")
