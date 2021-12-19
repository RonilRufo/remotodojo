import random
import urllib

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Post
from ..views import PostUpdate
from .mixins import PostsMixin


class PostUpdateTests(PostsMixin, TestCase):
    """
    Test cases for :view:`posts.PostUpdate`
    """

    def setUp(self):
        self.user = self.create_user()
        self.client.force_login(self.user)

    def test_update_post_get_request(self):
        """
        Test successful response in rendering update post page.
        """
        post = self.create_post(
            author=self.user,
            is_published=True,
            is_public=True,
        )
        url = reverse("posts:post-update", args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        form = response.context.get("form")
        self.assertIsInstance(form, PostForm)
        self.assertEqual(post, response.context.get("post"))

    def test_update_post_request(self):
        """
        Test successful update of a post of the logged in user.
        """
        post = self.create_post(
            author=self.user,
            is_published=True,
            is_public=True,
        )

        payload = {
            "content": self.fake.sentence(),
            "is_published": True,
            "is_public": True,
        }
        url = reverse("posts:post-update", args=(post.id,))
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("posts:post-list"))

        # Grab the post again to retrieve the latest changes
        post = Post.objects.get(id=post.id)
        self.assertEqual(post.content, payload["content"])
        self.assertEqual(post.is_published, payload["is_published"])
        self.assertEqual(post.is_public, payload["is_public"])

        # Test message after successfully updating a post.
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn(PostUpdate.success_message, messages)

    def test_update_post_unpublished_post(self):
        """
        Test successful update of a post making it unpublished. It will not be listed
        in the home page.
        """
        # Create random visible posts
        [
            self.create_post(is_published=True, is_public=True)
            for _ in range(random.randint(5, 10))
        ]

        post = self.create_post(
            author=self.user,
            is_published=True,
            is_public=True,
        )
        payload = {
            "content": post.content,
            "is_published": False,
            "is_public": post.is_public,
        }
        url = reverse("posts:post-update", args=(post.id,))
        list_url = reverse("posts:post-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, list_url)

        # Grab the post again to retrieve the latest changes
        post = Post.objects.get(id=post.id)
        self.assertFalse(post.is_published)

        response = self.client.get(list_url)
        posts = response.context.get("posts")
        self.assertNotIn(post, posts)

    def test_update_post_private_post(self):
        """
        Test successful update of a post making it private. It will not be listed in the
        home page.
        """
        # Create random visible posts
        [
            self.create_post(is_published=True, is_public=True)
            for _ in range(random.randint(5, 10))
        ]

        post = self.create_post(
            author=self.user,
            is_published=True,
            is_public=True,
        )
        payload = {
            "content": post.content,
            "is_published": post.is_published,
            "is_public": False,
        }
        url = reverse("posts:post-update", args=(post.id,))
        list_url = reverse("posts:post-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, list_url)

        # Grab the post again to retrieve the latest changes
        post = Post.objects.get(id=post.id)
        self.assertFalse(post.is_public)

        response = self.client.get(list_url)
        posts = response.context.get("posts")
        self.assertNotIn(post, posts)

    def test_update_post_get_request_unauthenticated_user(self):
        """
        Test redirect to login page if user is anonymous on GET requests.
        """
        self.client.logout()

        post = self.create_post(
            author=self.user,
            is_published=True,
            is_public=True,
        )
        update_url = reverse("posts:post-update", args=(post.id,))

        login_url = reverse("accounts:login")
        query_param = urllib.parse.urlencode({"next": update_url})
        login_redirect = f"{login_url}?{query_param}"
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, login_redirect)

    def test_update_post_post_request_unauthenticated_user(self):
        """
        Test redirect to login page if user is anonymous on POST requests.
        """
        self.client.logout()

        post = self.create_post(
            author=self.user,
            is_published=True,
            is_public=True,
        )
        update_url = reverse("posts:post-update", args=(post.id,))
        payload = {
            "content": self.fake.sentence(),
            "is_published": False,
            "is_public": False,
        }

        login_url = reverse("accounts:login")
        query_param = urllib.parse.urlencode({"next": update_url})
        login_redirect = f"{login_url}?{query_param}"
        response = self.client.post(update_url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, login_redirect)

        # Check that changes did not apply
        for key in payload.keys():
            self.assertNotEqual(getattr(post, key), payload[key])

    def test_update_post_get_request_not_owner(self):
        """
        Test not found response when trying to update a post that does not belong to the
        user in GET request.
        """
        user = self.create_user()
        post = self.create_post(
            author=user,
            is_published=True,
            is_public=True,
        )
        url = reverse("posts:post-update", args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update_post_request_not_owner(self):
        """
        Test not found response when trying to update a post that does not belong to the
        user in POST request.
        """
        user = self.create_user()
        post = self.create_post(author=user, is_published=True, is_public=True)

        payload = {
            "content": self.fake.sentence(),
            "is_published": True,
            "is_public": True,
        }
        url = reverse("posts:post-update", args=(post.id,))
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 404)
