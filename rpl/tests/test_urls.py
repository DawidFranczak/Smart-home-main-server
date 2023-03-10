from django.test import SimpleTestCase
from django.urls import reverse, resolve

from rpl.views import RplView


class TestRPLUrls(SimpleTestCase):

    def test_RPL_urls(self) -> None:
        url_rpl = reverse('rpl')

        self.assertEqual(resolve(url_rpl).func.view_class, RplView)
