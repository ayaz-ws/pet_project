from django.urls import path

from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, UserPostList, home_view

urlpatterns = [
    path("", home_view, name="home"),
    path("posts/", PostList.as_view(), name="posts"),
    path("posts/user/<int:pk>", UserPostList.as_view(), name="users_posts"),
    path("posts/<int:pk>", PostDetail.as_view(), name="post_detail"),
    path("posts/create/", PostCreate.as_view(), name="post_create"),
    path("posts/<int:pk>/update/", PostUpdate.as_view(), name="post_update"),
    path("posts/<int:pk>/delete", PostDelete.as_view(), name="post_delete"),
]
