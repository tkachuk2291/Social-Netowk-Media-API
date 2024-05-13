from django.shortcuts import render

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserSerializer, TokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogoutView(generics.DestroyAPIView):
    pass


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
