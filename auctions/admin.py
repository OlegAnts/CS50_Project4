from django.contrib import admin
from .models import Listing, User, UserListingRelation, Watchlist

# Register your models here.

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(UserListingRelation)
admin.site.register(Watchlist)
