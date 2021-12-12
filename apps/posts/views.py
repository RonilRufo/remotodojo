from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View
from django.views.generic.detail import SingleObjectMixin

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


class PostToggle(LoginRequiredMixin, SingleObjectMixin, View):
    """
    Toggles the `is_published` or `is_public` values depending on the sent form. Only
    accepts POST requests.
    """

    def get_success_url(self) -> str:
        """
        Redirects the request to the user's posts page upon success.
        """
        return reverse_lazy("posts:my-posts")

    def get_queryset(self):
        """
        Returns posts made by the logged in user.
        """
        return Post.objects.filter(author=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Handles the toggling of publish and public fields on POST request.
        """
        post: Post = self.get_object()
        if "toggle_publish" in request.POST:
            post.toggle_publish()
            action = "published" if post.is_published else "unpublished"
            messages.success(request, f'Successfully {action} the post: "{post.id}"')
        elif "toggle_public" in request.POST:
            post.toggle_public()
            action = "public" if post.is_public else "private"
            messages.success(request, f'Set the post "{post.id}" to {action}.')

        return HttpResponseRedirect(self.get_success_url())


class PostUserList(LoginRequiredMixin, ListView):
    """
    Displays all posts by the logged in user.
    """

    template_name = "posts/my_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        """
        Returns posts made by the logged in user.
        """
        return Post.objects.filter(author=self.request.user)


class PostDelete(LoginRequiredMixin, DeleteView):
    """
    Allows the author to delete his/her own post.
    """

    context_object_name = "post"
    success_url = reverse_lazy("posts:post-list")

    def get_queryset(self):
        """
        Returns posts made by the logged in user.
        """
        return Post.objects.filter(author=self.request.user)
