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
]
