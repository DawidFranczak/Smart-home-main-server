from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from .mod import data_for_chart

# Create your views here.


class ChartGetData(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "chart.html"

    def get_context_data(self, **kwargs):
        list_place = self.request.user.sensor_set.filter(fun="temp")

        if len(list_place) == 0:
            context = {"list_place": [_("No sensors have been added")]}
            return context
        context = data_for_chart(self.request, list_place)
        return context
