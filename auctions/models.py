from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class User(AbstractUser):
    pass

class Category(models.TextChoices):
    FASHION = 'FS', _('Fashion')
    TOYS = 'TY', _('Toys')
    ELECTRONIC = 'EL', _('Electronics')
    ANTIQUE = 'AN', _('Antique')
    HOME = 'HM', _('Home')
    OTHER = 'OT', _('Other')

class AuctionList(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images", default="images/default.jpg", blank=True)
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.OTHER)
    active = models.BooleanField(null=False, default=True)
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    def __str__(self):
        return f"{self.title} - {self.category}"

class Comment(models.Model):
    text = models.TextField(blank=True, default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank = True, null=True)
    auction = models.ForeignKey(AuctionList,on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"{self.text}"

class Bid(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    auction = models.ForeignKey(AuctionList, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"${self.price}"
    """auction = models.ForeignKey(AuctionList, models.CASCADE, related_name="auc", null=True, blank=True)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="ubid", null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="cmmt", null=True, blank=True)"""