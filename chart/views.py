from django.shortcuts import render
from .mod import data_for_chart
from django.views import View
# Create your views here.


class Chart(View):
    template_name = 'chart.html'

    def get(self, request):

        context = self.get_data(request)
        return render(request, self.template_name, context)

    def post(self, request):

        context = self.get_data(request)
        return render(request, self.template_name, context)

    @classmethod
    def get_data(cls, request):

        list_place = request.user.sensor_set.filter(fun='temp')
        if len(list_place) == 0:
            context = {}
            return render(request, cls.template_name, context)

        return data_for_chart(request, list_place)
