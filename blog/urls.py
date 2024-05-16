from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog.views import PostViewSet, PostListViewFollowingView, PostListUserView

router = DefaultRouter()

router.register("posts", PostViewSet, basename="posts")
urlpatterns = [path("", include(router.urls)),
               path("user-following/",PostListUserView.as_view(), name="post-following"),
               path("post-following/", PostListViewFollowingView.as_view(), name="post-following")
               ]

app_name = "blog"
