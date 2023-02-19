from django.db.models import Q
from datetime import datetime, timedelta


def data_for_chart(request):
    ''' 
    Get data and avarage temperature for chart from date to date
    '''

    data_from = request.POST.get('data-from')
    data_to = request.POST.get('data-to')
    place = request.POST.get("list")

    if not place:
        place = request.user.sensor_set.filter(fun='temp')[0]

    if data_from and data_to:

        format = '%Y-%m-%d'
        data_to = str(datetime.strptime(
            data_to[:19], format) + timedelta(days=1))
    else:
        data_from = datetime.now().date() - timedelta(days=6)
        data_to = str(datetime.now())

    data_average_temp_day = []
    data_average_temp_night = []
    data_average_data = []
    average_day = []
    average_night = []

    start_day = '06'
    end_day = '18'

    sensor = request.user.sensor_set.get(
        Q(fun='temp') &
        Q(name=place))

    temps = sensor.temp_set.filter(
        Q(time__gte=data_from) &
        Q(time__lte=data_to))

    # check is it any temperature measurment
    try:
        date = str(temps[0].time)[:10]  # e.g. 2023-02-11 without hour
    except IndexError:
        return {'list_place': request.user.sensor_set.filter(fun='temp')}

    for temp in temps:
        date = str(temp.time)[:10]

        # from 2023-02-15 22:00:00 to 22 (only hours)
        hour = str(temp.time).split().pop(1)[:2]

        if hour > start_day and hour <= end_day:
            average_day.append(float(temp.temp))
        else:
            average_night.append(float(temp.temp))

        if str(temp.time) == date + ' 23:00:00':
            data_average_temp_day.append(
                round(sum(average_day) / len(average_day), 2)
            )
            data_average_temp_night.append(
                round(sum(average_night) / len(average_night), 2)
            )
            data_average_data.append(date)

            average_day.clear()
            average_night.clear()

    context = {
        # only temperature values

        'data_temp': [temp.temp for temp in temps],
        # only data YYYY-MM-DD

        'data_time': [str(temp.time)[:16] for temp in temps],
        'data_average_temp_day': data_average_temp_day,
        'data_average_temp_night': data_average_temp_night,
        'data_average_data': data_average_data,
        'place': place,
        'list_place': request.user.sensor_set.filter(fun='temp')
    }
    return context
