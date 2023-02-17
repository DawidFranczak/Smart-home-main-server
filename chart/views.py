from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .mod import *
# Create your views here.


@login_required(login_url='login')
def chart(request):
    list_place = request.user.sensor_set.filter(fun='temp')

    if len(list_place) == 0:
        return render(request, 'chart.html')

    data_from = datetime.now().date() - timedelta(days=6)
    data_to = str(datetime.now())

    if request.method == 'POST':
        if request.POST["data-from"] and request.POST["data-to"]:

            data_from = request.POST["data-from"]
            data_to = request.POST["data-to"]
            format = '%Y-%m-%d'
            data_to = str(datetime.strptime(
                data_to[:19], format) + timedelta(days=1))

        place = request.POST["list"]
        context = data_for_chart(data_from, data_to, place, request)
        context['list_place'] = list_place

        return render(request, 'chart.html', context)

    place = list_place[0]
    context = data_for_chart(data_from, data_to, place, request)
    context['list_place'] = list_place

    return render(request, 'chart.html', context)
