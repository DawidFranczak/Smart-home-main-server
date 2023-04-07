import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from devices.models import Sensor

from .mod import stairs_settings


class StairsLoginRequirred(LoginRequiredMixin):
    login_url = "login"


class StairsGetAll(StairsLoginRequirred, TemplateView):
    """
    This class give all user's stairs

    endpoint: schody/
    """

    template_name = "stairs.html"

    def get_context_data(self):
        sensors = self.request.user.sensor_set.filter(fun="stairs")
        return {
            "sensors": sensors,
        }


class StairsUpdate(StairsLoginRequirred, View):
    """
    This class update selected stairs

    endpoint: schody/update/
    """

    def put(self, request) -> JsonResponse:
        get_data = json.loads(request.body)

        sensor = get_object_or_404(Sensor, pk=get_data["id"])
        stairs = sensor.stairs
        ngrok = request.user.ngrok.ngrok
        message, status = stairs_settings(get_data, sensor, stairs, ngrok)

        return JsonResponse(message, status=status)
