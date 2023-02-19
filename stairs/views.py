from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json
from .mod import send_data
# Create your views here.


class StairsView(View):
    template_name = 'stairs.html'

    def get(self, request):
        sensors = request.user.sensor_set.filter(fun='stairs')
        context = {
            "sensors": sensors,
        }
        return render(request, self.template_name, context)

    def post(self, request) -> JsonResponse:
        get_data = json.loads(request.body)

        sensor = request.user.sensor_set.get(pk=get_data['id'])
        stairs = sensor.stairs

        match get_data['action']:
            case 'set-lightingTime':

                stairs.lightTime = int(get_data['lightingTime'])
                message = 'te'+str(get_data['lightingTime'])

            case 'set-brightness':

                stairs.brightness = int(get_data['brightness'])
                message = 'bs'+str(get_data['brightness'])

            case 'set-step':

                stairs.steps = int(get_data['step'])
                message = 'sp'+str(get_data['step'])

            case 'change-stairs':

                if stairs.mode:
                    stairs.mode = False
                    message = 'OFF'
                else:
                    stairs.mode = True
                    message = 'ON'

        # Control simulation
        if sensor.name == 'tester':
            stairs.save()
            return JsonResponse({'success': True})
        # End simulation

        if send_data(message, sensor.ip, sensor.port):
            stairs.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})


# @login_required(login_url='login')
# def stairs(request):

#     if request.method == 'POST':
#         get_data = json.loads(request.body)

#         sensor = request.user.sensor_set.get(pk=get_data['id'])
#         stairs = sensor.stairs

#         match get_data['action']:
#             case 'set-lightingTime':

#                 stairs.lightTime = int(get_data['lightingTime'])
#                 message = 'te'+str(get_data['lightingTime'])

#             case 'set-brightness':

#                 stairs.brightness = int(get_data['brightness'])
#                 message = 'bs'+str(get_data['brightness'])

#             case 'set-step':

#                 stairs.steps = int(get_data['step'])
#                 message = 'sp'+str(get_data['step'])

#             case 'change-stairs':

#                 if stairs.mode:
#                     stairs.mode = False
#                     message = 'OFF'
#                 else:
#                     stairs.mode = True
#                     message = 'ON'

#         # Control simulation
#         if sensor.name == 'tester':
#             stairs.save()
#             return JsonResponse({'success': True})
#         # End simulation

#         if send_data(message, sensor.ip, sensor.port):
#             stairs.save()
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False})

#     sensors = request.user.sensor_set.filter(fun='stairs')
#     context = {
#         "sensors": sensors,
#     }
#     return render(request, 'stairs.html', context)
