from django.test import TransactionTestCase

from log.forms import CreateUserForm


class TestCreateUserForm(TransactionTestCase):
    def test_create_user_valid_form(self) -> None:
        form = CreateUserForm(
            data={
                "username": "tester",
                "password1": "dsawdsaw",
                "password2": "dsawdsaw",
                "email": "tester@tester.pl",
            }
        )
        self.assertTrue(form.is_valid())

    def test_create_user_does_valid_form(self) -> None:
        form = CreateUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
