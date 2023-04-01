from devices.models import Sensor
from django.contrib.auth.models import User
from django.test import Client, TransactionTestCase
from django.urls import resolve, reverse

from sunblind.views import CalibrationView, SunblindView


class TestUrls(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username="tester")
        self.user.set_password("tester12345")
        self.user.save()

        # Login user
        self.client = Client()
        self.client.login(username="tester", password="tester12345")

        return super().setUp()

    def test_list_resolve(self):
        url = reverse("sunblind")
        self.assertEqual(resolve(url).func.view_class, SunblindView)
        sensor_id = self.user.sensor_set.filter(fun="sunblind")[0].id
        url = reverse("calibration", args=[sensor_id])
        self.assertEqual(resolve(url).func.view_class, CalibrationView)
