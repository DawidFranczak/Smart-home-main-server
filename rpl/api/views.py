from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from log.models import Ngrok

@api_view(["POST"])
# /api/check/uid/
def checkUID(request):
    try:
        ngrok = request.data.get("url")
        ip = request.data.get("ip")
        uid = int(request.data.get("uid"))
        user = Ngrok.objects.get(ngrok=ngrok).user

        if not user.sensor_set.filter(ip = ip).exists():
            return Response({"success" : False})
        
        card = user.sensor_set.get(ip = ip).card_set.filter(uid = uid)
        return Response({
            "success": card.exists()
            })
    
    except ObjectDoesNotExist:
        return Response({
            "success": False,
        })

    except Exception as e:
        print(e)
        return redirect("home")


@api_view(["POST"])
# /api/check/lamp/
def checkLamp(request):
    try:
        ngrok = request.data.get("url")
        ip = request.data.get("ip")
        user = Ngrok.objects.get(ngrok=ngrok).user
        sensor_lamp_ip = user.sensor_set.get(ip = ip).rfid.lamp
        lamp = user.sensor_set.get(ip = sensor_lamp_ip)
        
        response = {
            "success": True,
            "ip": lamp.ip,
            "port": lamp.port
        }

        return Response(response)
    
    except ObjectDoesNotExist:
        return Response({
            "success": False,
        })
    except Exception as e:
        print(e)
        return redirect("home")