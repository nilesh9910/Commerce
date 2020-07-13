from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from .models import AuctionList
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

from .models import User, Category, Bid
from .forms import AuctionForm, BidForm


def index(request):
    a_list = AuctionList.objects.annotate(max_price=Max('bid__price'))
    context = {
        "a_list": a_list
    }
    return render(request, "auctions/index.html", context)


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

def createAuction(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            image = form.cleaned_data.get("image")
            category = form.cleaned_data.get('category')
            start_bid = form.cleaned_data.get('start_bid')
            if not image:
                image ="images/default.jpg"
            new_auc = request.user.auctionlist_set.create(title=title, description=description, image=image, category=category, active=True, start_bid=start_bid)
            new_auc.save()
            id=new_auc.id
            return HttpResponseRedirect(reverse("aucview", args=(id,)))
        else:
            return render(request, 'auctions/createauction.html', {'form': form})
    form = AuctionForm()
    return render(request, 'auctions/createauction.html', {'form': form})

def auction_view(request, id):
    try:
        auc = AuctionList.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404("Requested Auction is not Found")
    bids = auc.bid_set.all().order_by('-price')
    category = Category(auc.category).label
    max_bid = auc.bid_set.all().aggregate(Max('price'))
    if request.method =='POST':
        form = BidForm(request.POST)
        context = {'form': form, 'auc': auc, 'Category': category, "Bids": bids, "max_bid": max_bid['price__max']}
        if form.is_valid():
            bid_price = form.cleaned_data.get('bid_price')
            if max_bid['price__max']:
                if bid_price < max_bid['price__max']:
                    context['error']=f"Please select bid more than ${max_bid['price__max']}"
                    return render(request, 'auctions/auctionview.html', context)
            elif bid_price < auc.start_bid:
                context['error']=f"Please select bid more than ${auc.start_bid}"
                return render(request, 'auctions/auctionview.html', context)
            crbid = request.user.bid_set.create(price=bid_price, auction=auc)
            crbid.save()
            return render(request, 'auctions/auctionview.html', context)
    if request.GET.get('active') and request.GET['active']=='False':
        if request.user.is_authenticated and request.user.id==auc.user.id:
            auc.active=False
            auc.save()
    form = BidForm()
    max_bid = auc.bid_set.all().aggregate(Max('price'))
    context = {'form': form, 'auc': auc, 'Category': category, "Bids": bids, "max_bid": max_bid['price__max']}
    return render(request, 'auctions/auctionview.html', context)

def categories(request):
    return render(request, 'auctions/category.html')