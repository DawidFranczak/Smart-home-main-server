from django.test import TransactionTestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class TestSunblindView(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username="tester")
        self.user.set_password("tester12345")
        self.user.save()

        # Login user
        self.client = Client()
        self.client.login(username="tester", password="tester12345")

        # Sunblind url
        self.rpl_url = reverse("sunblind")

        return super().setUp()

    def test_GET_with_login(self) -> None:
        response = self.client.get(self.rpl_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sensors"]), 3)

    def test_updated_sunblind(self) -> None:
        # Sunblind exists
        sunblind_ip = self.user.sensor_set.filter(fun="sunblind")[0].id
        data = {"value": 50, "id": sunblind_ip}

        response = self.client.post(self.rpl_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 204)

        # Sunblind does't exists
        data = {"value": 50, "id": 743829}

        response = self.client.post(self.rpl_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_no_connection_with_home_server(self):
        sunblind_ip = self.user.sensor_set.filter(fun="sunblind")[1].id
        data = {"value": 50, "id": sunblind_ip}

        response = self.client.post(self.rpl_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 504)

    def test_GET_without_login(self) -> None:
        self.client.logout()
        response = self.client.get(self.rpl_url)
        self.assertEqual(response.status_code, 302)


class TestCalibrationView(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username="tester")
        self.user.set_password("tester12345")
        self.user.save()

        # Login user
        self.client = Client()
        self.client.login(username="tester", password="tester12345")

        # calibration url
        sensor_id = self.user.sensor_set.filter(fun="sunblind")[0].id
        self.calibration_url = reverse("calibration", args=[sensor_id])

        return super().setUp()

    def test_GET_with_login(self) -> None:
        response = self.client.get(self.calibration_url)
        self.assertEqual(response.status_code, 200)

    def test_sunblind_does_not_exists(self) -> None:
        calibration_url = reverse("calibration", args=[12345])
        response = self.client.get(calibration_url)
        self.assertEqual(response.status_code, 404)

    def test_calobration(self) -> None:
        list = [
            "up",
            "stop",
            "down",
            "stop",
            "save",
            "up",
            "stop",
            "down",
            "stop",
            "end",
        ]
        for i in list:
            data = {
                "action": i,
            }
            response = self.client.post(
                self.calibration_url, data, content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)

    def test_GET_without_login(self) -> None:
        self.client.logout()
        response = self.client.get(self.calibration_url)
        self.assertEqual(response.status_code, 302)
