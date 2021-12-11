from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom User model using email as username.
    """

    username = None
    email = models.EmailField(_("Email Address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")
