from django.test import TestCase
from django.urls import reverse

from ..forms import RegistrationForm
from ..models import CustomUser
from .mixins import AccountsMixin


class RegistrationTests(AccountsMixin, TestCase):
    """
    Test cases related to :view:`accounts.Registration`
    """

    def setUp(self):
        self.register_url = reverse("accounts:register")

    def test_register_get_request(self):
        """
        Test successful rendering of register page.
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get("form"), RegistrationForm)

    def test_register_post_request(self):
        """
        Test successful registration.
        """
        password = self.fake.password()
        payload = {
            "email": self.fake.email(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "password1": password,
            "password2": password,
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("posts:post-list"))

        self.assertIsNotNone(CustomUser.objects.get(email=payload["email"]))

    def test_register_email_already_taken(self):
        """
        Test raising ValidationError if the provided email is already taken.
        """
        user = self.create_user()
        password = self.fake.password()
        payload = {
            "email": user.email,
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "password1": password,
            "password2": password,
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, 200)

        form = response.context.get("form")
        self.assertIsNotNone(form.errors)
        self.assertIn("email", form.errors)

    def test_register_email_missing(self):
        """
        Test raising ValidationError if the email is missing.
        """
        password = self.fake.password()
        payload = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "password1": password,
            "password2": password,
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, 200)

        form = response.context.get("form")
        self.assertIsNotNone(form.errors)
        self.assertIn("email", form.errors)

    def test_register_first_name_missing(self):
        """
        Test raising ValidationError if the first name is missing.
        """
        password = self.fake.password()
        payload = {
            "email": self.fake.email(),
            "last_name": self.fake.last_name(),
            "password1": password,
            "password2": password,
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, 200)

        form = response.context.get("form")
        self.assertIsNotNone(form.errors)
        self.assertIn("first_name", form.errors)

    def test_register_last_name_missing(self):
        """
        Test raising ValidationError if the last name is missing.
        """
        password = self.fake.password()
        payload = {
            "email": self.fake.email(),
            "first_name": self.fake.first_name(),
            "password1": password,
            "password2": password,
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, 200)

        form = response.context.get("form")
        self.assertIsNotNone(form.errors)
        self.assertIn("last_name", form.errors)

    def test_register_passwords_do_not_match(self):
        """
        Test raising ValidationError if the passwords do not match
        """
        password = self.fake.password()
        payload = {
            "email": self.fake.email(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "password1": password,
            "password2": self.fake.password(),
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, 200)

        form = response.context.get("form")
        self.assertIsNotNone(form.errors)
        self.assertIn("password2", form.errors)
