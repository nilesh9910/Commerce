from django.contrib import admin
from .models import Bid, Category, AuctionList, User, Comment

# Register your models here.

admin.site.register(AuctionList)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Comment)