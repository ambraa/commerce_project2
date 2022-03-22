from django.contrib import admin


# Register your models here.
from .models import AuctionListings
admin.site.register(AuctionListings)

from .models import Watchlist
admin.site.register(Watchlist)

from .models import Comment
admin.site.register(Comment)
