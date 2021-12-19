import random
import urllib

from django.test import TestCase
from django.urls import reverse

from ..models import Post
from .mixins import PostsMixin


class PostUserListTests(PostsMixin, TestCase):
    """
    Test cases for :view:`posts.PostUserList`
    """

    def setUp(self):
        self.user = self.create_user()
        self.list_url = reverse("posts:my-posts")
        self.client.force_login(self.user)

    def test_post_user_list_get_request(self):
        """
        Test successful rendering of posts in post user list page.
        """
        visible_posts = [
            self.create_post(author=self.user) for _ in range(random.randint(5, 10))
        ]

        other_posts = [self.create_post() for _ in range(random.randint(3, 6))]

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        posts = response.context.get("posts")
        self.assertTrue(posts.exists())
        self.assertEqual(posts.count(), len(visible_posts))

        prev_post: Post = None
        for post in posts:
            self.assertIn(post, visible_posts)
            self.assertNotIn(post, other_posts)

            if prev_post is None:
                prev_post = post
                continue

            # Test content changed ordering
            self.assertGreater(prev_post.content_changed, post.content_changed)
            prev_post = post

    def test_post_user_list_get_request_unauthenticated_user(self):
        """
        Test successful redirect to login page if the user is authenticated.
        """
        self.client.logout()

        [self.create_post(author=self.user) for _ in range(random.randint(5, 10))]

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
        login_url = reverse("accounts:login")
        query_param = urllib.parse.urlencode({"next": self.list_url})
        login_redirect = f"{login_url}?{query_param}"
        self.assertRedirects(response, login_redirect)
