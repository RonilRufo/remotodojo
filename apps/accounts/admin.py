from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin view for :model:`accounts.CustomUser`
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("email", "first_name", "last_name", "is_superuser", "is_active")
    ordering = ("email",)
    search_fields = ("email", "last_name", "first_name")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        (
            "User Info",
            {
                "fields": (
                    "email",
                    "password",
                    ("first_name", "last_name"),
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
