from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from blog.models import Post, PostHashtags
from blog.permissions import IsOwnerOrReadOnly, IsAdminOrIfAuthenticatedReadOnly
from blog.serializers import PostSerializer, PostListSerializer, PostCreateSerializer, PostUpdateSerializer, \
    HashtagsSerializer, HashtagsListSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        title = self.request.query_params.get(
            "title"
        )
        content = self.request.query_params.get("content")
        author = self.request.query_params.get(
            "author"
        )
        hashtag = self.request.query_params.get(
            "hashtags"
        )

        queryset = self.queryset
        if title:
            queryset = queryset.filter(
                title__icontains=title
            )
        if content:
            queryset = queryset.filter(
                content__icontains=content
            )
        if author:
            queryset = queryset.filter(
                user__icontains=author
            )
        if hashtag:
            queryset = queryset.filter(
                hashtags__hashtags__icontains=hashtag
            )

        return queryset.distinct()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
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


class HashtagsView(viewsets.ModelViewSet):
    queryset = PostHashtags.objects.all().prefetch_related("hashtags")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    serializer_class = HashtagsSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return HashtagsListSerializer
        return HashtagsSerializer
