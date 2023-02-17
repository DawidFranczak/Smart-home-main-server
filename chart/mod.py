from django.db.models import Q


def data_for_chart(data_from, data_to, place, request):
    ''' 
    Get data and avarage temperature for chart from date to date
    '''

    data_temp = []
    data_time = []
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

    try:
        date_old = str(temps[0].time)[:10]
    except IndexError:
        return {}

    for temp in temps:
        date_new = str(temp.time)[:10]

        if str(temp.time) <= data_to and str(temp.time) >= str(data_from):
            data_temp.append(temp.temp)
            data_time.append(str(temp.time)[:16])
            hour = str(temp.time).split().pop(1)[:2]

            if hour > start_day and hour <= end_day:
                average_day.append(float(temp.temp))
            else:
                average_night.append(float(temp.temp))

            if date_new != date_old:

                data_average_temp_day.append(
                    round(sum(average_day) / len(average_day), 2)
                )
                data_average_temp_night.append(
                    round(sum(average_night) / len(average_night), 2)
                )
                data_average_data.append(date_old)

                average_day.clear()
                average_night.clear()
                date_old = date_new

    context = {
        'data_temp': data_temp,
        'data_time': data_time,
        'data_average_temp_day': data_average_temp_day,
        'data_average_temp_night': data_average_temp_night,
        'data_average_data': data_average_data,
        'place': place,
    }
    return context
