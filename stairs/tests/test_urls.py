from django.test import SimpleTestCase
from django.urls import resolve, reverse

from stairs.views import StairsView


class TestUrls(SimpleTestCase):
    def test_list_resolve(self):
        url = reverse("stairs")
        self.assertEqual(resolve(url).func.view_class, StairsView)
