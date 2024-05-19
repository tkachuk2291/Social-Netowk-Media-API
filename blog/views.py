from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from blog.models import Post, PostHashtags
from blog.permissions import (
    IsOwnerOrReadOnly,
    IsAdminOrIfAuthenticatedReadOnly,
)
from blog.serializers import (
    PostSerializer,
    PostListSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    HashtagsSerializer,
    HashtagsListSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        title = self.request.query_params.get("title")
        content = self.request.query_params.get("content")
        author = self.request.query_params.get("author")
        hashtag = self.request.query_params.get("hashtags")

        queryset = self.queryset
        if title:
            queryset = queryset.filter(title__icontains=title)
        if content:
            queryset = queryset.filter(content__icontains=content)
        if author:
            queryset = queryset.filter(user__email__icontains=author)
        if hashtag:
            queryset = queryset.filter(hashtags__hashtags__icontains=hashtag)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                description="Filter by title",
            ),
            OpenApiParameter(
                name="content",
                type=OpenApiTypes.STR,
                description="Filter by content",
            ),
            OpenApiParameter(
                name="author",
                type=OpenApiTypes.STR,
                description="Filter by author(user)",
            ),
            OpenApiParameter(
                name="hashtag",
                type=OpenApiTypes.STR,
                description="Filter by hashtag",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of posts and filtering for query_params 'title ,content , author ,hashtag '"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                description="Title of the post",
                required=True,
            ),
            OpenApiParameter(
                name="content",
                type=OpenApiTypes.STR,
                description="Content of the post",
                required=True,
            ),
            OpenApiParameter(
                name="hashtags",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                description="Hashtags associated with the post",
            ),
        ],
        request=PostCreateSerializer,
        responses={201: PostSerializer},
        description="Create a new post",
    )
    def create(self, request, *args, **kwargs):
        """Create a new post"""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=PostUpdateSerializer,
        responses={200: PostSerializer},
        description="Update an existing post",
    )
    def update(self, request, *args, **kwargs):
        """Update an existing post"""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=PostUpdateSerializer,
        responses={200: PostSerializer},
        description="Partially update an existing post",
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update an existing post"""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        request=PostSerializer,
        responses={204: None},
        description="Delete an existing post",
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an existing post"""
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return PostListSerializer
        elif self.action == "create":
            return PostCreateSerializer
        elif self.action == "retrieve":
            return PostSerializer
        elif self.action == "destroy":
            return PostSerializer
        return PostUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostListUserView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.users_posts.all()


class PostListViewFollowingView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostListSerializer

    def get_queryset(self):
        following_users = self.request.user.following.all()
        following_posts = Post.objects.filter(user__in=following_users)
        serializers = PostListSerializer(following_posts, many=True)
        return serializers.data

    def list(self, request, *args, **kwargs):
        """Get list of posts users'"""
        return super().list(request, *args, **kwargs)


class HashtagsView(viewsets.ModelViewSet):
    queryset = PostHashtags.objects.all().prefetch_related("hashtags")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    serializer_class = HashtagsSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return HashtagsListSerializer
        return HashtagsSerializer
