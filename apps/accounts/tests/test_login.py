from django.test import TestCase
from django.urls import reverse

from ..forms import LoginForm
from .mixins import AccountsMixin


class LoginTests(AccountsMixin, TestCase):
    """
    Test cases related to :view:`accounts.Login`
    """

    def setUp(self):
        self.login_url = reverse("accounts:login")

    def test_login_get_request(self):
        """
        Test successful rendering of login page.
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get("form"), LoginForm)

    def test_login_post_request(self):
        """
        Test successful response in logging in to the system.
        """
        user = self.create_user()
        password = self.fake.password()
        user.set_password(password)
        user.save()

        payload = {"username": user.email, "password": password}
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("posts:post-list"))
        self.assertEqual(response.wsgi_request.user, user)

    def test_login_email_does_not_exist(self):
        """
        Test raising ValidationError when email and password does not exist.
        """
        email = self.fake.email()
        password = self.fake.password()

        payload = {"username": email, "password": password}
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, 200)

        form = response.context.get("form")
        self.assertIsNotNone(form.errors)
        # __all__ for non-field errors
        self.assertIn("__all__", form.errors)

    def test_login_invalid_password(self):
        """
        Test raising ValidationError when password is incorrect.
        """
        password = self.fake.password()
        user = self.create_user()
        user.set_password(password)
        user.save()

        payload = {"username": user.email, "password": self.fake.password()}

        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, 200)

        form = response.context.get("form")
        self.assertIsNotNone(form.errors)
        # __all__ for non-field errors
        self.assertIn("__all__", form.errors)
