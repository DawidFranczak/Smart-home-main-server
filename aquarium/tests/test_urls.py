from django.test import SimpleTestCase
from django.urls import resolve, reverse

from aquarium.views import AquariumView


class TestUrls(SimpleTestCase):
    def test_list_resolve(self):
        url = reverse("aquarium")
        self.assertEqual(resolve(url).func.view_class, AquariumView)
