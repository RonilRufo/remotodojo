from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel, UUIDModel


class Post(TimeStampedModel, UUIDModel):
    """
    Stores a post/twit made by a specific user.

    Related to :model:`accounts.CustomUser`
    """

    content = models.CharField(max_length=255)
    content_changed = MonitorField(monitor="content")
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
        ordering = ("-modified",)

    def __str__(self) -> str:
        return f"{self.author}: {self.content[:50]}"

    def toggle_publish(self) -> None:
        """
        Toggles the value of `is_published` field from True to False or vice versa.
        """
        self.is_published = not self.is_published
        self.save(update_fields=["is_published"])

    def toggle_public(self) -> None:
        """
        Toggles the value of `is_public` field from True to False or vice versa.
        """
        self.is_public = not self.is_public
        self.save(update_fields=["is_public"])

    @property
    def is_visible_in_homepage(self) -> bool:
        """
        Posts are visible in homepage if they are both published and public.
        """
        return self.is_published and self.is_public
