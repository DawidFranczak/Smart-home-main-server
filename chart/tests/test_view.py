import datetime

from django.contrib.auth.models import User
from django.test import Client, TransactionTestCase
from django.urls import reverse


class TestView(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username="tester")
        self.user.set_password("haslo12345")
        self.user.save()

        # Login user
        self.client = Client()
        self.client.login(username="tester", password="haslo12345")

        self.chart_url = reverse("chart")
        return super().setUp()

    def test_GET_with_login(self) -> None:
        # Open / wykres with login user
        response = self.client.get(self.chart_url)
        self.assertEqual(response.status_code, 200)

        sensors = response.context["list_place"]
        self.assertEqual(len(sensors), 3)

        average_data = response.context["data_average_data"]
        self.assertEqual(len(average_data), 7)

    def test_POST_data_with_one_day(self):
        response = self.client.get(self.chart_url)
        sensor = response.context["list_place"][0]
        date = str(datetime.datetime.now())[:10]

        data = {
            "data-from": date,
            "data-to": date,
            "list": sensor.name,
        }
        response = self.client.post(self.chart_url, data)
        self.assertEqual(response.status_code, 200)
        data_average_from_one_day = response.context["data_average_data"]
        self.assertEqual(len(data_average_from_one_day), 1)

    def test_GET_without_login(self) -> None:
        # try open /wykres without login user -> redirect to login page
        self.client.logout()
        response = self.client.get(self.chart_url)
        self.assertEquals(response.status_code, 302)
