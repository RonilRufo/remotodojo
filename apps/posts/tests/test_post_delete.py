import urllib

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from ..models import Post
from ..views import PostDelete
from .mixins import PostsMixin


class PostDeleteTests(PostsMixin, TestCase):
    """
    Test cases for :view:`posts.PostDelete`
    """

    def setUp(self):
        self.user = self.create_user()
        self.client.force_login(self.user)

    def test_delete_post_get_request(self):
        """
        Test successful rendering of confirm delete page.
        """
        post = self.create_post(author=self.user)
        url = reverse("posts:post-delete", args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post, response.context.get("post"))

    def test_delete_post_request(self):
        """
        Test successfully deleting a post by the logged in user.
        """
        post = self.create_post(author=self.user)
        url = reverse("posts:post-delete", args=(post.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("posts:post-list"))
        self.assertRaises(Post.DoesNotExist, Post.objects.get, id=post.id)

        # Test message after successfully deleting a post.
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn(PostDelete.success_message, messages)

    def test_delete_post_get_request_unauthenticated_user(self):
        """
        Test successful redirect to login page if the user is not authenticated on GET
        request.
        """
        self.client.logout()

        post = self.create_post(author=self.user)
        url = reverse("posts:post-delete", args=(post.id,))
        response = self.client.get(url)

        login_url = reverse("accounts:login")
        query_param = urllib.parse.urlencode({"next": url})
        login_redirect = f"{login_url}?{query_param}"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, login_redirect)

    def test_delete_post_post_request_unauthenticated_user(self):
        """
        Test successful redirect to login page if the user is not authenticated on POST
        request.
        """
        self.client.logout()

        post = self.create_post(author=self.user)
        url = reverse("posts:post-delete", args=(post.id,))
        response = self.client.post(url)

        login_url = reverse("accounts:login")
        query_param = urllib.parse.urlencode({"next": url})
        login_redirect = f"{login_url}?{query_param}"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, login_redirect)

    def test_delete_post_get_request_not_owner(self):
        """
        Test not found response when trying to delete a post that does not belong to the
        user in GET request.
        """
        post = self.create_post()
        url = reverse("posts:post-delete", args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_post_post_request_not_owner(self):
        """
        Test not found response when trying to delete a post that does not belong to the
        user in POST request.
        """
        post = self.create_post()
        url = reverse("posts:post-delete", args=(post.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
