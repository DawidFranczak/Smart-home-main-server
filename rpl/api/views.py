from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from devices.models import Sensor
from log.models import Ngrok


@api_view(["POST"])
# /api/check/uid/
def check_uid(request):
    try:
        ngrok = request.data.get("url")
        ip = request.data.get("ip")
        uid = int(request.data.get("uid"))
        user = Ngrok.objects.get(ngrok=ngrok).user

        if not user.sensor_set.filter(ip=ip).exists():
            return Response({"success": False}, status=404)

        card = user.sensor_set.get(ip=ip).card_set.filter(uid=uid)
        return Response({"success": card.exists()}, status=200)

    except ObjectDoesNotExist:
        return Response({"success": False}, status=404)

    except Ngrok.DoesNotExist:
        return redirect("home")


@api_view(["POST"])
# /api/check/lamp/
def check_lamp(request):
    ngrok = request.data.get("url")
    ip = request.data.get("ip")

    try:
        user = Ngrok.objects.get(ngrok=ngrok).user
    except Ngrok.DoesNotExist:
        return redirect("home")
    try:
        sensor_lamp_ip = user.sensor_set.get(ip=ip).rfid.lamp
        lamp = user.sensor_set.get(ip=sensor_lamp_ip)
    except ObjectDoesNotExist:
        return {"success": False}

    response = {"success": True, "ip": lamp.ip, "port": lamp.port}

    return Response(response, status=200)


@api_view(["GET"])
# /api/rpl/lamp/get/id/
def get_lamp(request, id):
    lamp = get_object_or_404(Sensor, pk=id)
    rfids = request.user.sensor_set.filter(fun="rfid")
    buttons = request.user.sensor_set.filter(fun="btn")

    respond = {
        "rfid": [rfid.id for rfid in rfids if rfid.rfid.lamp == lamp.ip],
        "btn": [button.id for button in buttons if button.button.lamp == lamp.ip],
    }
    return JsonResponse(respond, status=200)
