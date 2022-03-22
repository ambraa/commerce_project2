from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

CATEGORY_CHOICES = (
        ("fashion", "Fashion"),
        ("toys", "Toys"),
        ("electronics", "Electronics"),
        ("home", "home"),
    )

class AuctionListings(models.Model):
    title = models.CharField(max_length=64,)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.URLField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    last_bid = models.IntegerField(blank=True, default=None)
    bidder = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True)

    def __str__(self):
        return f"{self.id}, {self.title}, {self.description}, {self.price}, {self.image}, {self.category}, {self.last_bid}, {self.bidder} "

class Bid(models.Model):
    user = models.CharField(max_length=64)
    bid = models.IntegerField(max_length=64, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    # id = models.ManyToManyField(AuctionListings, blank=True)

    def __str__(self):
        return f"{self.id}:{self.user}, {self.comment}, {self.date}"
    

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    product_id = models.IntegerField()

    