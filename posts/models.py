from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def liked(self):
        return

    @property
    def likes_count(self):
        return self.likes.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
