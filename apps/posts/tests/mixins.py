from apps.accounts.tests.mixins import AccountsMixin

from .. import models
from .factories import PostFactory


class PostsMixin(AccountsMixin):
    """
    Collection of helper methods to test objects related to posts app.
    """

    def create_post(self, **kwargs) -> models.Post:
        """
        Creates a dummy :model:`posts.Post` instance.
        """
        if "content" not in kwargs:
            kwargs.update({"content": self.fake.sentence()})

        if "author" not in kwargs:
            kwargs.update({"author": self.create_user()})

        return PostFactory.create(**kwargs)
