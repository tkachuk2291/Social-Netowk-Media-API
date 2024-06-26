import pathlib
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


def image_path(self, filename):
    filename = (
            f"{slugify(self.email)}-{uuid.uuid4()}"
            + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload/user/avatar") / pathlib.Path(filename)


class CustomUser(AbstractUser):
    username = None
    image = models.ImageField(upload_to=image_path, null=True)
    email = models.EmailField(_("email address"), unique=True)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        UniqueConstraint(fields=["email"], name="unique_email")
