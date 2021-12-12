from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, UUIDModel


class Post(TimeStampedModel, UUIDModel):
    """
    Stores a post/twit made by a specific user.

    Related to :model:`accounts.CustomUser`
    """

    content = models.CharField(max_length=255)
    author = models.ForeignKey(
        "accounts.CustomUser",
        related_name="posts",
        on_delete=models.CASCADE,
    )
    is_published = models.BooleanField(
        default=False,
        help_text=_("Only published posts will be displayed in the landing page."),
    )
    is_public = models.BooleanField(
        default=True,
        help_text=_(
            "Public posts can be viewed by everyone while private posts can only be "
            "seen by the author."
        ),
    )

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ("-created",)

    def __str__(self) -> str:
        return f"{self.author}: {self.content[:50]}"

    def publish(self) -> None:
        """
        Publishes the post. Sets the `is_published` field to True.
        """
        if not self.is_published:
            self.is_published = True
            self.save(update_fields=["is_published"])

    def make_private(self) -> None:
        """
        Sets the post to private. Only the user can see it.
        """
        if self.is_public:
            self.is_public = False
            self.save(update_fields=["is_public"])

    def make_public(self) -> None:
        """
        Sets the post to public. The post can be viewed by everyone.
        """
        if not self.is_public:
            self.is_public = True
            self.save(update_fields=["is_public"])
