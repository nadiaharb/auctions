from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(NewListing)
admin.site.register(Watchlist)
admin.site.register(WatchlistItem)
admin.site.register(Comment)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(ActiveListings)
admin.site.register(Category)
