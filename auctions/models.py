from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName


class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

    def __str__(self):
        return f"{self.bid}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image_url = models.URLField(max_length=2000, blank=True, null=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="price")
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userComment")
    comment = models.CharField(max_length=250)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listingComment")

    def __str__(self):
        return f"{self.author} commented on {self.listing}"
