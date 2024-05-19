from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "password", "image")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "password")


class UserCreateSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name")


class UserProfileSerializer(UserSerializer):
    class Meta:
        title = serializers.EmailField(
            validators=[
                UniqueValidator(queryset=get_user_model().objects.all())
            ]
        )
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}




class UserListSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name", "image")


class ApiRootSerializer(serializers.Serializer):
    user_list = serializers.HyperlinkedIdentityField(view_name="user-list")
    posts = serializers.HyperlinkedIdentityField(view_name="posts")


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "image")
