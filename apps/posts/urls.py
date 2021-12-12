"""
URL patterns in posts app
"""
from django.urls import path

from .views import (
    PostCreate,
    PostDelete,
    PostList,
    PostToggle,
    PostUpdate,
    PostUserList,
)

app_name = "posts"
urlpatterns = [
    path("", PostList.as_view(), name="post-list"),
    path("create/", PostCreate.as_view(), name="post-create"),
    path("delete/<uuid:pk>/", PostDelete.as_view(), name="post-delete"),
    path("update/<uuid:pk>/", PostUpdate.as_view(), name="post-update"),
    path("my-posts/", PostUserList.as_view(), name="my-posts"),
    path("toggle/<uuid:pk>/", PostToggle.as_view(), name="post-toggle"),
]
