from django.contrib.auth.models import AbstractUser
from django.db import models


class Post(models.Model):
    user = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    likes = models.IntegerField(default=0)
    is_liked = models.BooleanField(default=False) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes,
            "is_liked":self.is_liked
        }
    def __str__(self):
        return f"Created by {self.user}"
    

class User(AbstractUser):
    posts=models.ManyToManyField(Post, blank=True, related_name="posted_by")
    liked=models.ManyToManyField(Post, blank=True, related_name="liked_by")
    followers=models.ManyToManyField("self", blank=True,symmetrical=False, related_name="follower")
    followings=models.ManyToManyField("self", blank=True,symmetrical=False, related_name="following")

