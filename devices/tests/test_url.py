from django.test import SimpleTestCase
from django.urls import resolve, reverse
from devices.urls import DevicesView


class TestDevicesUrls(SimpleTestCase):
    def test_device_url(self):
        url = reverse("devices")
        self.assertEquals(resolve(url).func.view_class, DevicesView)
