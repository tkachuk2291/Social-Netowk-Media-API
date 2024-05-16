from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Post
        fields = ['title', "content", 'date', "author"]


class PostListSerializer(PostSerializer):
    class Meta:
        model = Post

        fields = ["id",'title', "content", 'date', "author"]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["user", 'date', 'title', "content", ]

