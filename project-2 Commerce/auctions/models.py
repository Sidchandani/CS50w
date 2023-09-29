from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext as _
#.strftime("%B %d, %Y")


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    created_by = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    price = models.IntegerField()
    desc = models.CharField(max_length=300)
    pub_date = models.DateField(_("Date"), auto_now_add=True)
    image = models.CharField(max_length=500,default="")
    closed = models.BooleanField(default=False)
    winner = models.CharField(max_length=50,default=False)

    def __str__(self):
        return self.product_name

class User(AbstractUser):
    WatchList=models.ManyToManyField(Product, blank=True, related_name="user")

class Bid(models.Model):
    prod=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bid")
    highest=models.FloatField(default=0)
    cnt=models.IntegerField(default=0)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")

    def __str__(self):
        return f"Highest Bid for {self.prod.product_name} is ${self.highest}."


class Comment(models.Model):
    comm=models.CharField(max_length=250)
    comm_date = models.DateField(_("Date"), auto_now_add=True)
    prod=models.ManyToManyField(Product, blank=True, related_name="comment")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")

    def __str__(self):
        return f"Comment by {self.user.username}."
