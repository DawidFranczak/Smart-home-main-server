from django.test import SimpleTestCase
from django.urls import resolve, reverse

from chart.views import chart


class TestUrl(SimpleTestCase):
    def test_url(self):
        url = reverse("chart")
        self.assertEquals(resolve(url).func, chart)
