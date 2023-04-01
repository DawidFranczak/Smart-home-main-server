from django.test import SimpleTestCase
from django.urls import resolve, reverse

from user_page.views import (UserChangeEmail, UserChangeImage, UserChangeNgrok,
                             UserChangePassword, UserDelete, UserPage)


class TestUrls(SimpleTestCase):
    def test_list_resolve(self):
        url_user_page = reverse("user_page")
        url_change_password = reverse("user_change_password")
        url_change_email = reverse("user_change_email")
        url_change_ngrok = reverse("user_change_url")
        url_change_image = reverse("user_change_image")
        url_delete = reverse("user_delete")

        self.assertEqual(resolve(url_user_page).func.view_class, UserPage)
        self.assertEqual(
            resolve(url_change_password).func.view_class, UserChangePassword
        )
        self.assertEqual(resolve(url_change_email).func.view_class, UserChangeEmail)
        self.assertEqual(resolve(url_change_ngrok).func.view_class, UserChangeNgrok)
        self.assertEqual(resolve(url_change_image).func.view_class, UserChangeImage)
        self.assertEqual(resolve(url_delete).func.view_class, UserDelete)
