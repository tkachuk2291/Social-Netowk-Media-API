from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='users_posts')
    title = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
