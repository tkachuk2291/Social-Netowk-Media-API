from django.urls import path

from .views import (
    UserListView,
    LogoutView,
    UserLoginView,
    UserProfile,
    UserRegisterView,
    FollowUserAPIView,
    UnfollowUserAPIView,
    FollowingList,
    FollowersList,
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users-list/", UserListView.as_view(), name="users-list"),
    path("user-profile/", UserProfile.as_view(), name="user-profile"),
    path("register/", UserRegisterView.as_view(), name="user-registration"),
    path(
        "follow/<int:user_id>/",
        FollowUserAPIView.as_view(),
        name="follow_user",
    ),
    path(
        "unfollow/<int:user_id>/",
        UnfollowUserAPIView.as_view(),
        name="unfollow-user",
    ),
    path("following-list", FollowingList.as_view(), name="following-user"),
    path("followers-list", FollowersList.as_view(), name="follow_user"),
]
