from django.test import TestCase, Client
from django.urls import reverse
from chart.views import Chart
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib import auth


class TestView(TestCase):

    def setUp(self) -> None:

        self.chart_url = reverse('chart')

        self.user = User.objects.create(username='tester-user')
        self.user.set_password('12345')
        self.user.save()

        self.client = Client()

    def test_GET_without_login(self) -> None:
        # try open /wykres without login user -> redirect to login page
        response = self.client.get(self.chart_url)
        self.assertEquals(response.status_code, 302)

    def test_GET_with_login(self) -> None:
        # check authenticate user
        self.client.login(username='tester-user', password='12345')
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, True)

        # try open /wykres wit login user
        response = self.client.get(self.chart_url)
        self.assertEquals(response.status_code, 200)

        # check amount of user's measurment devices
        temp_device = self.user.sensor_set.filter(fun='temp').count()
        self.assertEquals(temp_device, 3)
