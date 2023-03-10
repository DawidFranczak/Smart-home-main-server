from django.test import TransactionTestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class TestRplView(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username='tester')
        self.user.set_password('tester12345')
        self.user.save()

        # Login user
        self.client = Client()
        self.client.login(username='tester', password='tester12345')

        # Rpl url
        self.rpl_url = reverse('rpl')

        return super().setUp()

    def test_GET_with_login(self) -> None:

        response = self.client.get(self.rpl_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rfids']), 3)
        self.assertEqual(len(response.context['lamps']), 3)
        self.assertEqual(len(response.context['buttons']), 3)

    def test_GET_lamp(self) -> None:
        lamp_id = self.user.sensor_set.filter(fun='lamp')[0].id
        data = {
            'action': 'get',
            'id': lamp_id
        }

        response = self.client.post(
            self.rpl_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_connect_rfid_and_button_with_lamp(self) -> None:
        lamp_id = self.user.sensor_set.filter(fun='lamp')[0].id
        rfid_id = self.user.sensor_set.filter(fun='rfid')[0].id
        button_id = self.user.sensor_set.filter(fun='btn')[0].id
        data = {
            'action': 'connect',
            'lamp': lamp_id,
            'rfids': [rfid_id],
            'btns': [button_id],
        }

        response = self.client.post(
            self.rpl_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
