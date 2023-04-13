from django.urls import path
from django.contrib import admin

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:list_title>/", views.listing, name="listing"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_to_watchlist/<str:list_title>/", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<str:list_title>/", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("make_bid/<str:list_title>/", views.make_bid, name='make_bid')

]
