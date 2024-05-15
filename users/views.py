from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model, logout, authenticate
from django.views import View
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import UserSerializer, UserProfileSerializer, UserListSerializer


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
        # token = Token.objects.first()
        # print(token)
        # token.delete()
        # print("Request data:", request.data)
        logout(request)
        return Response({'message': "Logout successful"})
        # # token = Token.objects.get(key=request.data.get('key'))
        # token = Token.objects.get(key=request.data.get('key'))
        #
        # print(token, "TOKEN")
        # if token:
        #     print("Token not found")
        # token.delete()
        # return Response(status=status.HTTP_200_OK)


# class EmailTokenObtainPairView(TokenObtainPairView):
#     serializer_class = TokenObtainPairSerializer
class UserLoginView(APIView):
    serializer_class = UserSerializer

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
    queryset = get_user_model
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
