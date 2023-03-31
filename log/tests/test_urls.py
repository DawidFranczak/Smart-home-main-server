from django.test import SimpleTestCase
from django.urls import resolve, reverse

from log.views import home, user_login, user_logout, user_register


class TestLogUrls(SimpleTestCase):
    def test_log_urls(self) -> None:
        url_home = reverse("home")
        url_login = reverse("login")
        url_logout = reverse("logout")
        url_register = reverse("user_register")

        self.assertEqual(resolve(url_home).func, home)
        self.assertEqual(resolve(url_login).func, user_login)
        self.assertEqual(resolve(url_logout).func, user_logout)
        self.assertEqual(resolve(url_register).func, user_register)
