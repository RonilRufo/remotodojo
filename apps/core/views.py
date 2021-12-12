from typing import Any, Optional

from django.urls import reverse_lazy
from django.views.generic import RedirectView


class Index(RedirectView):
    """
    Redirects to the corresponding pages when index page is accessed.
    """

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        """
        Returns the URL to redirect to.
        """
        return reverse_lazy("posts:post-list")
