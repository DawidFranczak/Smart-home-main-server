from django.test import Client, TransactionTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import json


class TestStairsViews(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username="tester")
        self.user.set_password("haslo12345")
        self.user.save()

        # Login user
        self.client = Client()
        self.client.login(username="tester", password="haslo12345")

        # Select stairs
        self.stairs_id = self.user.sensor_set.filter(fun="stairs")[0].id

        # Stairs url
        self.stairs_url = reverse("stairs")

        return super().setUp()

    def test_stairs_list_get_authenticate_user(self) -> None:
        response = self.client.get(self.stairs_url)
        self.assertEqual(len(response.context["sensors"]), 3)
        self.assertEqual(response.status_code, 200)

    def test_stairs_get_settings(self) -> None:
        settings = self.client.get(f"/api/stairs/{self.stairs_id}")
        self.assertEqual(len(settings.json()), 5)

    def test_stairs_updated_settings(self) -> None:
        # Stairs exists
        data = {
            "action": "set-lightingTime",
            "lightingTime": 100,
            "id": self.stairs_id,
        }
        response = self.client.post(
            self.stairs_url, json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        # Stairs does'n exists

        data = {
            "action": "set-lightingTime",
            "lightingTime": 100,
            "id": 1245435,
        }
        response = self.client.post(
            self.stairs_url, json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)

    def test_stairs_list_get_anonymous_user(self) -> None:
        self.client.logout()
        response = self.client.get(self.stairs_url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/zaloguj/"))
