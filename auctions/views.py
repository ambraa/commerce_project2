from itertools import product
from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .models import User
from .models import AuctionListings, Bid, Comment, Watchlist
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm


class formCreateListing(ModelForm):
    class Meta:
        model = AuctionListings
        fields = ["title", "description", "price", "image", "category", "last_bid", "bidder"]

class formWatchlist(ModelForm):
    class Meta:
        model = Watchlist
        fields = ["user", "product_id"]

# class formComment(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ["user", "comment", "date"]



class formBid(ModelForm):
    class Meta:
        model = Bid
        fields = ["user", "bid", "date"]


def index(request):
    return render(request, "auctions/index.html",{
        "products": AuctionListings.objects.all()
    })
    
def addwatchlist(request, product_id):
    if request.method == "POST":
        item = Watchlist()
        item.user = request.user.username
        item.product_id = product_id
        item.save()
        product = AuctionListings.objects.get(id=product_id)
        watchlist = Watchlist.objects.filter(product_id=product_id, user = request.user.username)
        
        return render(request, "auctions/watchlist.html",{
        "product": product,
        "watchlist": watchlist
        })
        
    else: 
        return render(request, "auctions/listing.html", {
            "form": formWatchlist()
        })
   


@login_required
def watchlist(request):
    items = Watchlist.objects.filter(user = request.user.username)
    products = []
    for item in items:
        products.append(AuctionListings.objects.get(id=item.product_id))
    empty = False
    if len(products) == 0:
        empty = True
    
    return render(request, "auctions/watchlist.html", {
        "empty": empty,
        "products": products
    })


def create_listing(request):
    if request.method == "POST":
        form = formCreateListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            bidder = form.cleaned_data["bidder"]
            last_bid = form.cleaned_data["last_bid"]
            product = AuctionListings(title=title, description=description, image=image, price=price, category=category, bidder=bidder, last_bid=last_bid)
            product.save()
    else: 
        return render(request, "auctions/create_listing.html", {
            "form": formCreateListing()
            
        }) 
           
    return render(request, "auctions/create_listing.html", {
            "form": formCreateListing()
        })  

def listing(request, product_id):
    product = AuctionListings.objects.get(pk=product_id)
    return render(request, "auctions/listing.html", {
        "product": product
    })


def newbid(request, product_id):
    if request.method == "POST":
            newbid = int(request.POST.get("newbid"))
            product = AuctionListings.objects.get(pk=product_id)
            bid = product.price
            if newbid <= bid:
                return render(request, "auctions/listing.html", {
                    "product": product,
                    "message": "Your bid should be bigger than the current one."
                })
            else:
                product.price = newbid
                product.save()
                objBid = Bid()
                
                objBid.user = request.user.username
                objBid.bid = newbid
                objBid.save()
                return render(request, "auctions/listing.html", {
                    "product": product,
                    "message": "Your bid is successfully added.",
                })

   


    





# 
   




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




def categories(request):
    return render(request, "auctions/categories.html",{
        "categories": CATEGORY_CHOICES
    })


def category(request, category):
    products = AuctionListings.objects.all()

    sameProducts = []

    for product in products:
        if product.category == category:
            sameProducts.append(product)
            empty = False
            if len(products) == 0:
                empty = True

    

    return render(request, "auctions/category.html", {
        "products": sameProducts,
        "category": category,
        "empty":empty
    })
