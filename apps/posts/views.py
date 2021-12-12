from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import PostForm
from .models import Post


class PostList(ListView):
    """
    Displays all visible posts to the user.
    """

    queryset = Post.objects.filter(is_published=True, is_public=True)
    context_object_name = "posts"
    template_name = "posts/list.html"


class PostCreate(LoginRequiredMixin, CreateView):
    """
    Displays a form that lets users create a post. Users must be authenticated to use
    this page.
    """

    model = Post
    form_class = PostForm
    template_name = "posts/create.html"

    def get_success_url(self) -> str:
        """
        Overrides the success URL so it redirects to homepage.
        """
        return reverse_lazy("posts:post-list")

    def form_valid(self, form):
        """
        Assign the logged in user as author of the post when form is valid.
        """
        post = form.save(commit=False)
        post.author = self.request.user
        self.object = post.save()
        return HttpResponseRedirect(self.get_success_url())


class PostUpdate(LoginRequiredMixin, UpdateView):
    """
    Allows the author to update his/her own post.
    """

    form_class = PostForm
    template_name = "posts/update.html"
    context_object_name = "post"
    success_url = reverse_lazy("posts:post-list")

    def get_queryset(self):
        """
        Returns posts made by the logged in user.
        """
        return Post.objects.filter(author=self.request.user)
