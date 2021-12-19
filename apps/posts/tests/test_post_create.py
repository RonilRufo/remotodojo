import urllib

from django.test import TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Post
from .mixins import PostsMixin


class PostCreateTests(PostsMixin, TestCase):
    """
    Test cases for :view:`posts.PostCreate`
    """

    def setUp(self):
        self.create_url = reverse("posts:post-create")
        self.user = self.create_user()
        self.client.force_login(self.user)

    def test_create_post_get_request(self):
        """
        Test successful response in rendering create post page.
        """
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

        form = response.context.get("form")
        self.assertIsInstance(form, PostForm)

    def test_create_post_home_page_redirect(self):
        """
        Test successful creation of a public post and redirects to the home page.
        """
        payload = {
            "content": self.fake.sentence(),
            "is_published": True,
            "is_public": True,
        }
        response = self.client.post(self.create_url, payload)
        self.assertTrue(self.user.posts.exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("posts:post-list"))

    def test_create_post_unpublished_redirect(self):
        """
        Test successful creation of an unpublished post and redirects to my posts page.
        """
        payload = {
            "content": self.fake.sentence(),
            "is_published": False,
            "is_public": True,
        }
        response = self.client.post(self.create_url, payload)
        self.assertTrue(self.user.posts.exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("posts:my-posts"))

    def test_create_post_private_redirect(self):
        """
        Test successful creation of a private post and redirects to my posts page.
        """
        payload = {
            "content": self.fake.sentence(),
            "is_published": True,
            "is_public": False,
        }
        response = self.client.post(self.create_url, payload)
        self.assertTrue(self.user.posts.exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("posts:my-posts"))

    def test_create_post_get_request_unauthenticated_user(self):
        """
        Test redirect to login page if user is anonymous on GET requests.
        """
        self.client.logout()

        login_url = reverse("accounts:login")
        query_param = urllib.parse.urlencode({"next": self.create_url})
        login_redirect = f"{login_url}?{query_param}"
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, login_redirect)

        # Check that no post has been created
        self.assertFalse(Post.objects.exists())

    def test_create_post_post_request_unauthenticated_user(self):
        """
        Test redirect to login page if user is anonymous on POST requests.
        """
        self.client.logout()

        payload = {
            "content": self.fake.sentence(),
            "is_published": True,
            "is_public": True,
        }

        login_url = reverse("accounts:login")
        query_param = urllib.parse.urlencode({"next": self.create_url})
        login_redirect = f"{login_url}?{query_param}"
        response = self.client.post(self.create_url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, login_redirect)

        # Check that no post has been created
        self.assertFalse(Post.objects.exists())
