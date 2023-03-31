from datetime import datetime, timedelta
from statistics import fmean

from django.db.models import Q


def data_for_chart(request, list_place):
    """
    Get data and avarage temperature for chart from date to date
    """

    data_from = request.POST.get("data-from")
    data_to = request.POST.get("data-to")
    place = request.POST.get("list")

    if not place:
        place = list_place[0]

    if data_from and data_to:
        format = "%Y-%m-%d"
        data_to = str(datetime.strptime(data_to[:19], format) + timedelta(days=1))
    else:
        data_from = datetime.now().date() - timedelta(days=7)
        data_to = str(datetime.now())

    data_average_temp_day = []
    data_average_temp_night = []
    data_average_data = []
    average_day = []
    average_night = []

    start_day = 6
    end_day = 18

    sensor = request.user.sensor_set.get(Q(fun="temp") & Q(name=place))

    temps = sensor.temp_set.filter(Q(time__gte=data_from) & Q(time__lte=data_to))

    # check is it any temperature measurment

    try:
        date = temps[0].time.day  # e.g. 2023-02-11 without hour
    except IndexError:
        return {"list_place": list_place}

    for temp in temps:
        date = str(temp.time)[:10]
        hour = temp.time.hour

        if hour > start_day and hour <= end_day:
            average_day.append(float(temp.temp))
        else:
            average_night.append(float(temp.temp))

        if temp.time.hour == 23 and len(average_day) and len(average_night):
            data_average_temp_day.append(round(fmean(average_day), 2))
            data_average_temp_night.append(round(fmean(average_night), 2))
            data_average_data.append(date)
            average_day.clear()
            average_night.clear()

    context = {
        # only temperature values
        "data_temp": [temp.temp for temp in temps],
        # only data YYYY-MM-DD
        "data_time": [str(temp.time)[:16] for temp in temps],
        "data_average_temp_day": data_average_temp_day,
        "data_average_temp_night": data_average_temp_night,
        "data_average_data": data_average_data,
        "place": place,
        "list_place": list_place,
    }
    return context
