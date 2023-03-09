from django.test import Client, TransactionTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import json


class TestAquariumViews(TransactionTestCase):

    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username='tester')
        self.user.set_password('haslo12345')
        self.user.save()

        # Login user
        self.client = Client()
        self.client.login(username='tester', password='haslo12345')

        # Select aquarium
        self.aquarium_id = self.user.sensor_set.filter(fun='aqua')[0].id

        # Aquarium url
        self.aquarium_url = reverse('aquarium')

        return super().setUp()

    def test_aquarium_list_get_authenticate_user(self) -> None:

        response = self.client.get(self.aquarium_url)

        self.assertEqual(len(response.context['aquas']), 3)
        self.assertEqual(response.status_code, 200)

    def test_aquarium_get_settings(self) -> None:

        settings = self.client.get(f'/api/aquarium/{self.aquarium_id}')
        self.assertEqual(len(settings.json()), 9)

    def test_aquarium_updated_settings(self) -> None:

        data = {
            "action": "changeRGB",
            "r": 100,
            "g": 100,
            "b": 100,
            "id": self.aquarium_id,
        }
        response = self.client.post(self.aquarium_url, json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_aquarium_list_get_anonymous_user(self) -> None:
        self.client.logout()
        response = self.client.get(self.aquarium_url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/zaloguj/'))
