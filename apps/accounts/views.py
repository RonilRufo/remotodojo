from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import LoginForm


class Login(LoginView):
    """
    Handles user authentication.
    """

    template_name = "accounts/login.html"
    authentication_form = LoginForm

    def get_success_url(self) -> str:
        """
        Returns the redirect URL upon successful login.
        """
        return reverse_lazy("posts:post-list")
