from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, AuctionListing, Comment, Bid

def add_bid(request, id):
    newBid = request.POST['addBid']
    listingParameters = AuctionListing.objects.get(pk=id)
    isInWatchlist = request.user in listingParameters.watchlist.all()
    comments = Comment.objects.filter(listing=listingParameters)
    if float(newBid) > listingParameters.price.bid:
        updateBid = Bid(user=request.user, bid=newBid)
        updateBid.save()
        listingParameters.price = updateBid
        listingParameters.save()
        return render(request, "auctions/listing.html", {
            'listing': listingParameters,
            'message': "Bid was updated",
            'update': True,
            'isInWatchlist': isInWatchlist,
            'comments': comments
        })
    else:
        return render(request, "auctions/listing.html", {
            'listing': listingParameters,
            'message': "Fail while adding a bid",
            'update': False,
            'isInWatchlist': isInWatchlist,
            'comments': comments
        })

def add_comment(request, id):
    currentUser = request.user
    listingParameters = AuctionListing.objects.get(pk=id)
    content = request.POST['newComment']
    comment = Comment(
        author=currentUser,
        comment = content,
        listing = listingParameters
    )
    comment.save()
    
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def listing_view(request, id):
    listingParameters = AuctionListing.objects.get(pk=id)

    print("Listing Title:", listingParameters.title)
    print("Image URL:", listingParameters.image_url)
    print("Listing description:", listingParameters.description)
    print("Price:", listingParameters.price)
    print("Is listing active:", listingParameters.is_active)
    print("Posted by:", listingParameters.user)
    print("Winner:", listingParameters.winner)

    isInWatchlist = request.user in listingParameters.watchlist.all()
    comments = Comment.objects.filter(listing=listingParameters)
    return render(request, "auctions/listing.html", {
        'listing': listingParameters,
        'isInWatchlist': isInWatchlist,
        'comments': comments
    })

@login_required
def watchlist_display(request):
    currentUser = request.user
    listings = currentUser.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        'listings': listings,
    })


def watchlist_add(request, id):
    listingParameters = AuctionListing.objects.get(pk=id)
    currentUser = request.user
    listingParameters.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchlist_remove(request, id):
    listingParameters = AuctionListing.objects.get(pk=id)
    currentUser = request.user
    listingParameters.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def filter_category(request):
    if request.method == "POST":
        chosenCategory = request.POST["category"]
        category = Category.objects.get(categoryName=chosenCategory)
        categories = Category.objects.all()
        activeListings = AuctionListing.objects.filter(is_active=True, category=category)
        return render(request, "auctions/index.html", {
            'listings': activeListings,
            'categories': categories
        })


def index(request):
    listings = AuctionListing.objects.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings,
        'categories': categories
    })


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

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


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        price = request.POST["price"]
        #is_active = request.POST["is_active"]
        category = request.POST.get("category")
        user = request.user

        categoryData = Category.objects.get(categoryName=category)
        bid = Bid(bid=float(price), user=user)
        bid.save()
        listing = AuctionListing(
            title=title,
            description=description,
            image_url=image_url,
            price=bid,
            category=categoryData,
            user=user
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })

@login_required
def close_auction(request, id):
    # Get the listing object
    listing = AuctionListing.objects.get(pk=id)
    comments = Comment.objects.filter(listing=listing)

    if request.user == listing.user:
        if listing.is_active:
            highest_bid = listing.price

            listing.winner = highest_bid.user
            listing.is_active = False
            listing.save()

            return render(request, "auctions/listing.html", {
                'listing': listing,
                'update': True,
                'message': 'Listing successfully updated.',
                'comments': comments
            })
        else:
            return render(request, 'auctions/listing.html', {
                'message': 'This listing is already closed.',
                'listing': listing,
                'comments': comments
            })
    else:
        return render(request, 'auctions/listing.html', {
            'message': 'You are not allowed to close this auction.',
            'listing': listing,
            'comments': comments
        })