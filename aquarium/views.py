from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .mod import *

# Create your views here.


class AquariumView(View):
    template_name = 'aquarium.html'

    def get(self, request, *args, **kwargs):
        aquas = request.user.sensor_set.filter(fun='aqua')
        context = {
            'aquas': aquas
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        response = aquarium_contorler(request)

        return JsonResponse(response)
