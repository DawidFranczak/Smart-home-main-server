from django.contrib.auth.models import User
from django.test import Client, TransactionTestCase
from django.urls import reverse


class TestLightViews(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username="tester")
        self.user.set_password("tester12345")
        self.user.save()

        # Login user
        self.client = Client()
        self.client.login(username="tester", password="tester12345")

        # Ligth url
        self.light_url = reverse("light")

        return super().setUp()

    def test_GET_with_login(self) -> None:
        response = self.client.get(self.light_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sensors"]), 3)

    def test_ON_OFF_light(self) -> None:
        # Test turn on -> test lamp
        light_id = self.user.sensor_set.filter(fun="light")[0].id
        data = {
            "action": "change",
            "id": light_id,
        }

        response = self.client.post(
            self.light_url, data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # Test turn on -> lamp does exists lamp
        data = {
            "action": "change",
            "id": 8549,
        }

        response = self.client.post(
            self.light_url, data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

        # Test turn on -> no connected lamp
        light_id = self.user.sensor_set.filter(fun="light")[1].id
        data = {
            "action": "change",
            "id": light_id,
        }

        response = self.client.post(
            self.light_url, data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)
