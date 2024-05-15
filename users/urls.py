from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from .views import UserListView ,LogoutView, UserLoginView, UserProfile, UserRegisterView , follow_user , unfollow_user

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user-list/', UserListView.as_view(), name='user_list'),
    path('user-profile/', UserProfile.as_view(), name='user_list'),
    path("register/", UserRegisterView.as_view(), name="user-registration"),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
]
