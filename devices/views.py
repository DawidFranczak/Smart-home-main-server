import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.views.generic.edit import DeleteView

from .mod import add_sensor, add_sensor_tester, add_uid, delete_sensor
from .models import Card, Sensor


class DeviceAuthMixins(LoginRequiredMixin):
    login_url = "login"
    template_name = "devices.html"


class DevicesGetAll(DeviceAuthMixins, TemplateView):
    def get_context_data(self, **kwargs):
        sensors = self.request.user.sensor_set.all()

        context = {
            "sensors": [
                {
                    "fun": sensor.fun,
                    "name": sensor.name,
                    "id": sensor.id,
                    "cards": [
                        {"id": card.id, "name": card.name}
                        for card in sensor.card_set.all()
                    ]
                    if sensor.fun == "rfid"
                    else "",
                }
                for sensor in sensors
            ]
        }

        return context


class DeviceAdd(DeviceAuthMixins, View):
    def post(self, request):
        get_data = json.loads(request.body)
        # Simulation adding sensors
        if get_data["name"] == "tester":
            message, status = add_sensor_tester(get_data, request)
            return JsonResponse(message, status=status)
        # End simulation

        if get_data["fun"] == "uid":
            message, status = add_uid(get_data, request.user)
        else:
            message, status = add_sensor(get_data, request.user)

        return JsonResponse(message, status=status)


class DevicesDelete(DeviceAuthMixins, DeleteView):
    model = Sensor
    success_url = "/urzadzenia/"
    template_name = "confirm_delete.html"


class DevicesCardDelete(DeviceAuthMixins, DeleteView):
    model = Card
    success_url = "/urzadzenia/"
    template_name = "confirm_delete.html"
