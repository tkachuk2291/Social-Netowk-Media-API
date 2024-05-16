from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog.views import PostViewSet, PostListViewFollowingView, PostListUserView, HashtagsView

router = DefaultRouter()

router.register("posts", PostViewSet, basename="posts")
router.register("post-hashtags", HashtagsView, basename="hashtags")

urlpatterns = [path("", include(router.urls)),
               path("user-following/", PostListUserView.as_view(), name="post-following"),
               path("post-following/", PostListViewFollowingView.as_view(), name="post-following"),
               ]

app_name = "blog"
