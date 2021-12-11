from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin view for :model:`posts.Post`
    """

    list_display = (
        "author",
        "get_content_display",
        "created",
        "modified",
    )

    def get_content_display(self, obj: models.Post) -> str:
        """
        Trims the content for admin display.
        """
        return obj.content[:50]

    get_content_display.short_description = _("Content")
