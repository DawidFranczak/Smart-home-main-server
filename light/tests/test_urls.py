from django.test import SimpleTestCase
from django.urls import reverse, resolve

from light.views import LightView


class TestLightUrl(SimpleTestCase):
    def test_light_url(self):
        url = reverse("light")
        self.assertEquals(resolve(url).func.view_class, LightView)
