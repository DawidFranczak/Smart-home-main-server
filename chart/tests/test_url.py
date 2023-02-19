from django.test import SimpleTestCase
from django.urls import reverse, resolve
from chart.views import Chart


class TestUrl(SimpleTestCase):

    def test_url(self):
        url = reverse('chart')
        self.assertEquals(resolve(url).func.view_class, Chart)
