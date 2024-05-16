from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import include, path, reverse
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView

from blog.models import Post
from blog.serializers import PostSerializer, PostListSerializer, PostCreateSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == "create":
            return PostCreateSerializer
        return PostSerializer


class PostListUserView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        print(self.request.user.users_posts.all())
        return self.request.user.users_posts.all()


class PostListViewFollowingView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        following_users = self.request.user.following.all()
        following_posts = Post.objects.filter(user__in=following_users)
        serializers = PostListSerializer(following_posts, many=True)
        return serializers.data
