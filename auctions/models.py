from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORIES = [
        ("NC", "No Category"),
        ("TS", "Toys"),
        ("FN", "Fashion"),
        ("EL", "Electronics"),
        ("FD", "Food")
    ]

    list_title = models.CharField(max_length=20, primary_key=True, null=False)
    list_description = models.TextField(max_length=100, default='Empty description')
    list_category = models.CharField(max_length=20, choices=CATEGORIES, default="No Category")
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2, default='1.00')

    list_image_URL = models.URLField(default="https://www.tharagold.in/assets/img/no-product-found.png")

    list_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.list_title}"


# class Bid(models.Model):
#     pass


# class Comment(models.Model):
#     pass
