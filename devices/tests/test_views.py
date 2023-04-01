from django.contrib.auth.models import User
from django.test import Client, TransactionTestCase
from django.urls import reverse


class DevicesViewsTest(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username="tester")
        self.user.set_password("haslo12345")
        self.user.save()

        # Login user
        self.client = Client()
        self.client.login(username="tester", password="haslo12345")

        self.devices_url = reverse("devices")
        return super().setUp()

    def test_GET_with_login(self) -> None:
        response = self.client.get(self.devices_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["sensors"]))

    def test_add_sensor(self):
        data = {
            "fun": "temp",
            "name": "tester",
        }
        response = self.client.post(
            self.devices_url, data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 417)

        data = {
            "fun": "sunblind",
            "name": "tester",
        }
        response = self.client.post(
            self.devices_url, data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_delete_sensor(self):
        id = self.user.sensor_set.all()[1].id
        data = {
            "id": id,
        }
        response = self.client.delete(
            self.devices_url, data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        data = {
            "id": 8477489342,
        }
        response = self.client.delete(
            self.devices_url, data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)

    def test_GET_without_login(self) -> None:
        self.client.logout()
        response = self.client.get(self.devices_url)
        self.assertEqual(response.status_code, 302)
