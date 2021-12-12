from django.views.generic import ListView

from .models import Post


class PostList(ListView):
    """
    Displays all visible posts to the user.
    """

    queryset = Post.objects.filter(is_published=True, is_public=True)
    context_object_name = "posts"
    template_name = "posts/list.html"
