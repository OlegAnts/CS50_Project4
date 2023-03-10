from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all(),
        "listing": listing,
        # "title": listing.list_title,
        # "description": listing.list_description,
        # "owner": listing.list_owner,
        # "bid": listing.starting_bid,
        # "category": listing.get_list_category_display(),
        # "image": listing.list_image_URL
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, list_title):
    listing = Listing.objects.get(pk=list_title)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "title": listing.list_title,
        "description": listing.list_description,
        "owner": listing.list_owner,
        "bid": listing.starting_bid,
        "category": listing.get_list_category_display(),
        "image": listing.list_image_URL
    })


def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        bid = request.POST.get("bid")
        category = request.POST.get("category")
        image = request.POST.get("image")

        user = request.user

        new_listing = Listing(list_title=title, list_description=description, list_category=category,
                              starting_bid=bid, list_image_URL=image, list_owner=user)

        new_listing.save()
    return render(request, "auctions/create_listing.html")
