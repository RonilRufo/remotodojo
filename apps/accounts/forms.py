from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class LoginForm(AuthenticationForm):
    """
    custom authentication form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control form-control-user"

        self.fields["username"].widget.attrs["placeholder"] = "Enter Email Address..."
        self.fields["username"].widget.attrs["aria-describedby"] = "emailHelp"
        self.fields["password"].widget.attrs["placeholder"] = "Password"


class RegistrationForm(UserCreationForm):
    """
    Form to be used in registration.
    """

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control form-control-user"
            self.fields[field].widget.attrs["placeholder"] = self.fields[
                field
            ].label.title()
