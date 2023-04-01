from django.test import SimpleTestCase
from django.urls import resolve, reverse

from log.views import Home, UserLogin, UserLogout, UserRegister


class TestLogUrls(SimpleTestCase):
    def test_log_urls(self) -> None:
        url_home = reverse("home")
        url_login = reverse("login")
        url_logout = reverse("logout")
        url_register = reverse("user_register")

        self.assertEqual(resolve(url_home).func.view_class, Home)
        self.assertEqual(resolve(url_login).func.view_class, UserLogin)
        self.assertEqual(resolve(url_logout).func.view_class, UserLogout)
        self.assertEqual(resolve(url_register).func.view_class, UserRegister)
