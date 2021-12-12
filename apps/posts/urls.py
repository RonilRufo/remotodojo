"""
URL patterns in posts app
"""
from django.urls import path

from .views import PostCreate, PostList

app_name = "posts"
urlpatterns = [
    path("", PostList.as_view(), name="post-list"),
    path("create/", PostCreate.as_view(), name="post-create"),
]
