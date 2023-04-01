from django.contrib.auth.models import User
from django.test import TransactionTestCase

from user_page.forms import (ChangeEmailForm, ChangeNgrokForm,
                             ChangePasswordForm)


class TestChangePasswordForm(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username="tester")
        self.user.set_password("tester12345")
        self.user.save()

        return super().setUp()

    def test_change_password_valid_form(self) -> None:
        form = ChangePasswordForm(
            user=self.user,
            data={
                "old_password": "tester12345",
                "new_password1": "dsawdsaw2",
                "new_password2": "dsawdsaw2",
            },
        )
        self.assertTrue(form.is_valid())

    def test_change_password_does_valid_form(self) -> None:
        form = ChangePasswordForm(user=self.user, data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


class TestChangeEmailForm(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username="tester", email="test@test.pl")
        self.user.set_password("tester12345")
        self.user.save()

        return super().setUp()

    def test_change_email_valid_form(self) -> None:
        form = ChangeEmailForm(
            user=self.user,
            data={
                "new_email": "test2@test.pl",
            },
        )
        self.assertTrue(form.is_valid())

    def test_change_email_does_valid_form(self) -> None:
        form = ChangeEmailForm(user=self.user, data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class TestChangeNgrokForm(TransactionTestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username="tester")
        self.user.set_password("tester12345")
        self.user.save()

        return super().setUp()

    def test_change_url_valid_form(self) -> None:
        form = ChangeNgrokForm(
            user=self.user,
            data={
                "new_link": "https://www.test.pl",
            },
        )
        self.assertTrue(form.is_valid())

    def test_change_url_does_valid_form(self) -> None:
        form = ChangeNgrokForm(
            user=self.user,
            data={
                "new_link": "hps://www.test.pl",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
