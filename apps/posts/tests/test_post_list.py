import random

from django.test import TestCase
from django.urls import reverse

from .mixins import PostsMixin


class PostListTests(PostsMixin, TestCase):
    """
    Test cases for :view:`posts.PostList`
    """

    def setUp(self):
        self.list_url = reverse("posts:post-list")

    def test_post_list_get_request(self):
        """
        Test successful rendering of posts in post list page.
        """
        visible_posts = [
            self.create_post(is_published=True, is_public=True)
            for _ in range(random.randint(5, 10))
        ]

        unpublished_posts = [
            self.create_post(is_published=False, is_public=True)
            for _ in range(random.randint(5, 10))
        ]

        private_posts = [
            self.create_post(is_published=True, is_public=False)
            for _ in range(random.randint(5, 10))
        ]

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        posts = response.context.get("posts")
        self.assertTrue(posts.exists())
        self.assertEqual(posts.count(), len(visible_posts))
        for post in posts:
            self.assertIn(post, visible_posts)
            self.assertNotIn(post, unpublished_posts)
            self.assertNotIn(post, private_posts)
