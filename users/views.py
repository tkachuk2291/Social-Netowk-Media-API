from django.contrib.auth import get_user_model, logout, authenticate
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import (UserSerializer,
                               UserProfileSerializer,
                               UserListSerializer,
                               UserLoginSerializer
                               )


class UserListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer

    def get_queryset(self):
        email = self.request.query_params.get(
            "email"
        )
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get(
            "last_name"
        )
        queryset = self.queryset
        if email:
            queryset = queryset.filter(
                email__icontains=email
            )
        if first_name:
            queryset = queryset.filter(
                first_name__icontains=first_name
            )
        if last_name:
            queryset = queryset.filter(
                last_name__icontains=last_name
            )
        return queryset.distinct()


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return Response({'message': "Logout successful"})


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class UserProfile(generics.RetrieveUpdateAPIView):
    queryset = get_user_model()
    user = get_user_model()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class FollowUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            user_to_follow = get_user_model().objects.get(id=user_id)
            user = request.user
            user.following.add(user_to_follow)
            return Response(status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UnfollowUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            user_to_unfollow = get_user_model().objects.get(id=user_id)
            user = request.user
            user.following.remove(user_to_unfollow)
            return Response(status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowingList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        serializers = UserListSerializer(following_users, many=True)
        return Response(serializers.data)


class FollowersList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        followers_users = user.followers.all()
        serializers = UserListSerializer(followers_users, many=True)
        return Response(serializers.data)
