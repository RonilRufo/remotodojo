from faker import Faker

from .. import models
from .factories import CustomUserFactory


class AccountsMixin:
    """
    Collection of helper methods needed to test objects related to accounts app.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.fake = Faker()
        super().__init__(*args, **kwargs)

    def create_user(self, **kwargs) -> models.CustomUser:
        """
        Returns a dummy :model:`accounts.CustomUser` instance.
        """
        if "email" not in kwargs:
            kwargs.update({"email": self.fake.email()})

        if "first_name" not in kwargs:
            kwargs.update({"first_name": self.fake.first_name()})

        if "last_name" not in kwargs:
            kwargs.update({"last_name": self.fake.last_name()})

        return CustomUserFactory.create(**kwargs)
