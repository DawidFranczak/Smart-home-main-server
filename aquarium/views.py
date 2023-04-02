import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import View

from .mod import (
    change_fluo_lamp_state,
    change_fluo_lamp_time,
    change_led_state,
    change_led_time,
    change_mode,
    change_rgb,
)
from .tester import aquarium_contorler_tester

# Create your views here.


class AquariumView(View):
    template_name = "aquarium.html"

    def get(self, request):
        aquas = request.user.sensor_set.filter(fun="aqua")
        context = {
            "aquas": aquas,
        }
        return render(request, self.template_name, context, status=200)

    def post(self, request):
        get_data = json.loads(request.body)
        sensor = request.user.sensor_set.get(pk=get_data["id"])
        ngrok = request.user.ngrok.ngrok

        # Control simulation
        if sensor.name == "tester":
            aquarium_contorler_tester(request, sensor.aqua)
            return JsonResponse({"message": _("Settings updated successfully")})
        # End simulation

        match get_data["action"]:
            case "changeRGB":
                response = change_rgb(sensor, ngrok, get_data)

            case "changeFluoLampState":
                response = change_fluo_lamp_state(sensor, ngrok, get_data["value"])

            case "changeLedState":
                response = change_led_state(sensor, ngrok, get_data["value"])

            case "changeLedTime":

                data = {
                    "led_start": get_data["ledStart"],
                    "led_stop": get_data["ledStop"],
                }

                response = change_led_time(sensor, ngrok, data)

            case "changeFluoLampTime":

                data = {
                    "fluo_lamp_start": get_data["fluoLampStart"],
                    "fluo_lamp_stop": get_data["fluoLampStop"],
                }
                response = change_fluo_lamp_time(sensor, ngrok, data)

            case "changeMode":
                response = change_mode(sensor, ngrok, get_data["mode"])
                if get_data["mode"] and not response:
                    return JsonResponse(
                        {"fluo": sensor.aqua.fluo_mode, "led": sensor.aqua.led_mode},
                    )

        if response:
            return JsonResponse({"message": _("Settings updated successfully")})
        return JsonResponse({"message": _("No connection with aquarium")})
