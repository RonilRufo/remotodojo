"""
URL patterns in posts app
"""
from django.urls import path

from .views import PostCreate, PostList, PostUpdate, PostUserList

app_name = "posts"
urlpatterns = [
    path("", PostList.as_view(), name="post-list"),
    path("create/", PostCreate.as_view(), name="post-create"),
    path("update/<uuid:pk>/", PostUpdate.as_view(), name="post-update"),
    path("my-posts/", PostUserList.as_view(), name="my-posts"),
]
