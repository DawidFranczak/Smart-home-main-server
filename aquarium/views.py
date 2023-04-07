import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import ListView

from devices.models import Sensor

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


class AquariumGetAll(LoginRequiredMixin, ListView):
    """
    This class give all user's aquariums

    endpoint: akwaria/
    """

    login_url = "login"
    model = Sensor
    template_name = "aquarium.html"
    context_object_name = "aquas"

    def get_queryset(self):
        user = self.request.user
        filters = {"user": user, "fun": "aqua"}
        return super().get_queryset().filter(**filters)


class AquariumUpdate(LoginRequiredMixin, View):
    """
    This class update selected aquarium

    endpoint: akwaria/update
    """

    login_url = "login"
    template_name = "aquarium.html"

    def put(self, request):
        get_data = json.loads(request.body)
        sensor = request.user.sensor_set.get(pk=get_data["id"])
        ngrok = request.user.ngrok.ngrok

        # Control simulation
        if sensor.name == "tester":
            response = aquarium_contorler_tester(request, sensor.aqua)
            return JsonResponse(response)
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
