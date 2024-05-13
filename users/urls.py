from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import EmailTokenObtainPairView, RegisterView, LogoutView, ListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='token_obtain_pair'),
    path('user-list/', ListView.as_view(), name='user_list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/obtain/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
