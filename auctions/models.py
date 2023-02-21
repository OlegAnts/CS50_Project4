from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORIES = [
        ("NC", "No Category"),
        ("TS", "Toys"),
        ("FN", "Fashion"),
        ("EL", "Electronics")
    ]

    list_title = models.CharField(max_length=20, null=True)
    list_description = models.TextField(max_length=100, default='Empty description')
    list_category = models.CharField(max_length=20, choices=CATEGORIES, default="No Category")

    def __str__(self):
        return f"{self.list_title}"


# class Bid(models.Model):
#     pass


# class Comment(models.Model):
#     pass
