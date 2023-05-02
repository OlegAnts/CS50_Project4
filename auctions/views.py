from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing, UserListingRelation, Watchlist, Comment


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


@login_required()
def watchlist(request):
    user = request.user
    listings = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "listing": listing,
    })


@login_required()
def add_to_watchlist(request, list_title):
    if request.method == "POST":
        listing = Listing.objects.get(pk=list_title)
        user = request.user
        if not user.user_watchlist.filter(listing=list_title):
            Watchlist(user=request.user, listing=listing, in_watchlist=True).save()
            return HttpResponseRedirect(reverse("listing", kwargs={"list_title": list_title}))
        else:
            print("Already Exist")


@login_required()
def remove_from_watchlist(request, list_title):
    if request.method == "POST":
        listing = Listing.objects.get(pk=list_title)
        user = request.user
        db_exist = user.user_watchlist.filter(listing=list_title)
        if db_exist:
            db_exist.delete()
        else:
            print("Not in Watchlist")
    return HttpResponseRedirect(reverse("listing", kwargs={"list_title": list_title}))


def make_comment(request, list_title):
    if request.method == "POST":
        listing = Listing.objects.get(pk=list_title)
        user = request.user
        comment_text = request.POST.get('comment_text')
        new_comment = Comment(user=user, listing=listing, comment_text=comment_text)
        new_comment.save()
        return HttpResponseRedirect(reverse("listing", kwargs={"list_title": list_title}))



def listing(request, list_title):
    listing = Listing.objects.get(pk=list_title)
    watchlist_status = ''
    user = request.user
    owner = Listing.objects.get(list_title=list_title).list_owner
    list_status = "Open" if listing.list_winner is None else "Cloased"
    comments = Comment.objects.filter(listing=listing)
    # list_comments = []
    # for comment in comments:
    #     list_comments.append(comment.comment_text)

    try:
        current_bid = UserListingRelation.objects.filter(listing=list_title).order_by("-bid_price")[0].bid_price
        current_bid_buyer = UserListingRelation.objects.filter(listing=list_title).order_by("-bid_price")[0].user
    except Exception:
        current_bid = listing.starting_bid
        current_bid_buyer = listing.list_owner

    if request.user.is_authenticated:
        watchlist = request.user.user_watchlist.filter(listing=list_title)
        if watchlist:
            watchlist_status = "Product in your Watchlist"
        else:
            watchlist_status = "Product not in Watchlist"
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "title": listing.list_title,
        "description": listing.list_description,
        "owner": listing.list_owner,
        "bid": listing.starting_bid,
        "category": listing.get_list_category_display(),
        "image": listing.list_image_URL,
        "listing_status": list_status,
        'watchlist': watchlist_status,
        'current_bid': current_bid,
        'current_bid_buyer': current_bid_buyer,
        'listing_winner': listing.list_winner,
        'comments': comments
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


def make_bid(request, list_title):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(list_title=list_title)
        try:
            current_bid = UserListingRelation.objects.filter(listing=list_title).order_by("-bid_price")[0].bid_price
        except Exception:
            current_bid = listing.starting_bid
        bid = request.POST['new_bid']

        if float(bid) > current_bid:
            try:
                user_last_bid = UserListingRelation.objects.get(user=user, listing=listing)
                user_last_bid.bid_price = float(bid)
                user_last_bid.save()
            except Exception:
                new_bid = UserListingRelation(user=user, listing=listing, bid_price=bid)
                new_bid.save()
            finally:
                messages.success(request, 'Your Bid is success')
        else:
            messages.error(request, 'Your bid mast be more then current bid!')
    return HttpResponseRedirect(reverse("listing", kwargs={"list_title": list_title}))


def close_listing(request, list_title):
    current_bid = UserListingRelation.objects.filter(listing=list_title).order_by("-bid_price")[0]
    winner = current_bid.user
    listing = Listing.objects.get(list_title=list_title)
    listing.list_winner = winner
    listing.save()


    return HttpResponseRedirect(reverse("listing", kwargs={"list_title": list_title}))
