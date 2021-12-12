from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import LoginForm, RegistrationForm


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


class Registration(FormView):
    """
    Allows the user to register an account.
    """

    template_name = "accounts/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("posts:post-list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
