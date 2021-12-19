import urllib

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from ..models import Post
from .mixins import PostsMixin


class PostToggleTests(PostsMixin, TestCase):
    """
    Test cases for :view:`posts.PostToggle`
    """

    def setUp(self):
        self.user = self.create_user()
        self.client.force_login(self.user)

    def test_toggle_post_is_published(self):
        """
        Test successful response in toggling `is_published` value of the post.
        """
        post = self.create_post(
            author=self.user,
            is_published=True,
            is_public=True,
        )
        payload = {"toggle_publish": True}
        url = reverse("posts:post-toggle", args=(post.id,))
        response = self.client.post(url, payload)

        # Grab the post again to retrieve the latest changes
        post = Post.objects.get(id=post.id)
        self.assertFalse(post.is_published)
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Successfully unpublished the post", messages[0])

        # Send the request again to toggle another value
        response = self.client.post(url, payload)
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Successfully published the post", messages[1])

        # Grab the post again to retrieve the latest changes
        post = Post.objects.get(id=post.id)
        self.assertTrue(post.is_published)

    def test_toggle_post_is_public(self):
        """
        Test successful response in toggling `is_public` value of the post.
        """
        post = self.create_post(
            author=self.user,
            is_published=True,
            is_public=True,
        )
        payload = {"toggle_public": True}
        url = reverse("posts:post-toggle", args=(post.id,))
        response = self.client.post(url, payload)

        # Grab the post again to retrieve the latest changes
        post = Post.objects.get(id=post.id)
        self.assertFalse(post.is_public)
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("to private", messages[0])

        # Send the request again to toggle another value
        response = self.client.post(url, payload)

        # Grab the post again to retrieve the latest changes
        post = Post.objects.get(id=post.id)
        self.assertTrue(post.is_public)
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("to public", messages[1])

    def test_toggle_post_redirect_to_homepage(self):
        """
        Test successful redirect to home page after toggling value of a post.
        """
        post = self.create_post(
            author=self.user,
            is_published=True,
            is_public=True,
        )
        payload = {"toggle_published": True, "from_homepage": True}
        url = reverse("posts:post-toggle", args=(post.id,))
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("posts:post-list"))

    def test_toggle_post_redirect_to_my_posts(self):
        """
        Test successful redirect to my posts page after toggling value of a post.
        """
        post = self.create_post(
            author=self.user,
            is_published=True,
            is_public=True,
        )
        payload = {"toggle_published": True, "from_my_posts": True}
        url = reverse("posts:post-toggle", args=(post.id,))
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("posts:my-posts"))

    def test_toggle_post_unauthenticated_user(self):
        """
        Test successful redirect to login page if user is not authenticated.
        """
        self.client.logout()

        post = self.create_post(
            author=self.user,
            is_published=True,
            is_public=True,
        )
        payload = {"toggle_published": True, "from_my_posts": True}
        url = reverse("posts:post-toggle", args=(post.id,))
        response = self.client.post(url, payload)

        login_url = reverse("accounts:login")
        query_param = urllib.parse.urlencode({"next": url})
        login_redirect = f"{login_url}?{query_param}"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, login_redirect)

    def test_toggle_post_not_owner(self):
        """
        Test raising not found error when toggle post value that is not owned by the
        logged in user.
        """
        post = self.create_post(is_published=True, is_public=True)
        payload = {"toggle_published": True, "from_my_posts": True}
        url = reverse("posts:post-toggle", args=(post.id,))
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 404)
