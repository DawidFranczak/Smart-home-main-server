from django.contrib.auth.models import User
from django.test import Client, TransactionTestCase
from django.urls import reverse


class TestHomeView(TransactionTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url_home = reverse("home")
        return super().setUp()

    def test_GET_home_view_without_login(self) -> None:
        response = self.client.get(self.url_home)
        self.assertEqual(response.status_code, 302)

    def test_GET_home_view_witg_login(self) -> None:
        user = User.objects.create(username="tester")
        user.set_password("tester12345")
        user.save()
        self.client.login(username="tester", password="tester12345")
        response = self.client.get(self.url_home)
        self.assertEqual(response.status_code, 200)


class TestLoginViews(TransactionTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url_login = reverse("login")
        return super().setUp()

    def test_user_does_not_exist_login(self):
        data = {
            "username": "tester12345",
            "password": "dsawdsaw",
        }

        response = self.client.post(
            self.url_login, data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_user_exist_login(self):
        user = User.objects.create(username="tester12345")
        user.set_password("dsawdsaw")
        user.save()

        data = {
            "username": "tester12345",
            "password": "dsawdsaw",
        }

        response = self.client.post(self.url_login, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_user_without_all_data_login(self):
        user = User.objects.create(username="tester12345")
        user.set_password("dsawdsaw")
        user.save()

        data = {
            "username": "",
            "password": "dsawdsaw",
        }

        response = self.client.post(self.url_login, data)
        self.assertEqual(response.status_code, 302)


class TestLogoutView(TransactionTestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester12345")
        user.set_password("dsawdsaw")
        user.save()

        self.client = Client()
        self.client.login(username="tester12345", password="dsawdsaw")
        self.url_logout = reverse("logout")
        self.url_home = reverse("home")

        return super().setUp()

    def test_user_logout(self) -> None:
        # check user is login
        response = self.client.get(self.url_home)
        self.assertEqual(response.status_code, 200)

        # logout user
        response = self.client.get(self.url_logout)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/zaloguj/")

        # try to g on the home page without login
        response = self.client.get(self.url_home)
        self.assertEqual(response.status_code, 302)
