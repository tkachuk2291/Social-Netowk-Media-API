from rest_framework import serializers

from blog.models import Post, PostHashtags


class HashtagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostHashtags
        fields = ["id", "hashtags"]


class HashtagsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostHashtags
        fields = ["id", "hashtags"]


class PostSerializer(serializers.ModelSerializer):
    hashtags = HashtagsListSerializer(many=True)

    author = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Post
        fields = ["title", "content", "date", "author", "hashtags"]


class PostListSerializer(PostSerializer):
    class Meta:
        model = Post

        fields = ["id", "title", "content", "date", "author", "hashtags"]


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Post
        fields = ["date", "title", "content", "hashtags", "author"]


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "hashtags"]
