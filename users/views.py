from django.contrib.auth import get_user_model, logout, authenticate
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from users.serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserListSerializer,
    UserLoginSerializer, UserImageSerializer,
)


class UserListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        email = self.request.query_params.get("email")
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if email:
            queryset = queryset.filter(email__icontains=email)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="email",
                type=OpenApiTypes.STR,
                description="Filter by email",
            ),
            OpenApiParameter(
                name="first_name",
                type=OpenApiTypes.STR,
                description="Filter by first name",
            ),
            OpenApiParameter(
                name="last_name",
                type=OpenApiTypes.STR,
                description="Filter by last name",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        """Get list of users and filter by query parameters 'email', 'first_name', 'last_name'."""
        return self.list(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            200: OpenApiResponse(description="Successfully logged out."),
        },
        description="Logout the currently authenticated user.",
    )
    def get(self, request):
        logout(request)
        return Response(
            {"detail": "Logout successful"}, status=status.HTTP_200_OK
        )


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="email",
                type=OpenApiTypes.STR,
                description="User's email address for authentication.",
            ),
            OpenApiParameter(
                name="password",
                type=OpenApiTypes.STR,
                description="User's password for authentication.",
            ),
        ]
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=401)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    user = get_user_model()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == list:
            return UserSerializer
        elif self.action == "upload_image":
            return UserImageSerializer
        return UserSerializer

    @action(methods=["POST"], detail=False, url_path="upload-image")
    def upload_image(self, request):
        images = self.get_object()
        serializer = self.get_serializer(images, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class FollowUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=dict, description="Successfully followed the user."
            ),
            404: OpenApiResponse(
                response=dict, description="User not found."
            ),
        },
        description="Follow another user by their ID",
    )
    def get(self, request, user_id):
        try:
            user_to_follow = get_user_model().objects.get(id=user_id)
            user = request.user
            user.following.add(user_to_follow)
            return Response(
                {
                    "detail": f"Successfully followed the user {user_to_follow}"
                },
                status=status.HTTP_200_OK,
            )
        except get_user_model().DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class UnfollowUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=dict, description="Successfully unfollowed for user"
            ),
            404: OpenApiResponse(
                response=dict, description="User not found."
            ),
        },
        description="Unfollow another user by their ID",
    )
    def get(self, request, user_id):
        try:
            user_to_unfollow = get_user_model().objects.get(id=user_id)
            user = request.user
            user_unfollow = user.following.remove(user_to_unfollow)
            return Response(
                {
                    "detail": f"Successfully unfollowed for user {user_unfollow}"
                },
                status=status.HTTP_200_OK,
            )
        except get_user_model().DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class FollowingList(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses=UserListSerializer(many=True),
        description="Get a list of users that the authenticated user is following.",
    )
    def get(self, request):
        user = request.user
        following_users = user.following.all()
        serializers = UserListSerializer(following_users, many=True)
        return Response(serializers.data)


class FollowersList(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses=UserListSerializer(many=True),
        description="Get a list of followers for request user",
    )
    def get(self, request):
        user = request.user
        followers_users = user.followers.all()
        serializers = UserListSerializer(followers_users, many=True)
        return Response(serializers.data)
