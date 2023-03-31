from django.test import TransactionTestCase, Client, SimpleTestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TestUserPage(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username="tester")
        self.user.set_password("tester12345")
        self.user.save()

        # Login user
        self.client = Client()
        self.client.login(username="tester", password="tester12345")

        # Urls
        urls = [
            "user_page",
            "user_change_password",
            "user_change_email",
            "user_change_url",
            "user_change_image",
            "user_delete",
        ]
        self.user_page_url = [reverse(url) for url in urls]

        return super().setUp()

    def test_GET_with_login(self) -> None:
        for url in self.user_page_url:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_GET_without_login(self) -> None:
        self.client.logout()
        for url in self.user_page_url:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
