from datetime import datetime, timedelta
from statistics import fmean

from django.db.models import Q


def data_for_chart(request: object, list_place: list) -> dict:
    """
    This function calculates the average temperature values during
    the day and night within the given time range from the given sensor.

    :params request: This is incoming request.
    :params ngrok: This is the list of added temperature sensors.


    :return:  dictionary like below
            {
                "data_temp": a list of temperature measured every hour,
                "data_time": a list of the hours when the measurements were taken,
                "data_average_temp_day": a list of the average temperature at day,
                "data_average_temp_night": a list of the average temperature at night,
                "data_average_data": a list of dates with average measurement values,
                "place": a place from where come above calculations
                "list_place": a list of added sensors
            }
    """

    data_from = request.GET.get("data-from")
    data_to = request.GET.get("data-to")
    place = request.GET.get("list")

    if not place:
        place = list_place[0]

    if not data_from and not data_to:
        data_from = datetime.now().date() - timedelta(days=7)
        data_to = datetime.now()

    data_average_temp_day = []
    data_average_temp_night = []
    data_average_data = []
    average_day = []
    average_night = []

    start_day = 6
    end_day = 18

    sensor = request.user.sensor_set.get(Q(fun="temp") & Q(name=place))

    temps = sensor.temp_set.filter(Q(time__gte=data_from) & Q(time__lte=data_to))

    try:
        date = temps[0].time.day
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
        "data_temp": [temp.temp for temp in temps],
        "data_time": [str(temp.time)[:16] for temp in temps],
        "data_average_temp_day": data_average_temp_day,
        "data_average_temp_night": data_average_temp_night,
        "data_average_data": data_average_data,
        "place": place,
        "list_place": list_place,
    }
    return context
