from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.TextChoices):
    FASHION = 'FS', _('Fashion')
    TOYS = 'TY', _('Toys')
    ELECTRONIC = 'EL', _('Electronics')
    ANTIQUE = 'AN', _('Antique')
    HOME = 'HM', _('Home')
    OTHER = 'OT', _('Other')

class Bid(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Comment(models.Model):
    text = models.TextField(blank=False, default="")


class AuctionList(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images")
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.OTHER)
    active = models.BooleanField(null=False, default=False)
    start_bid = models.OneToOneField(Bid, on_delete=models.CASCADE)
    all_bids = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bids")

class User(AbstractUser):
    auction = models.ForeignKey(AuctionList, models.CASCADE, related_name="auc")
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="ubid")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="cmmt")