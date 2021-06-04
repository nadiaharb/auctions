from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import CreateNewListing, AddComment, AddBid
from .models import *


def index(request):
    return render(request, "auctions/activelistings.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("activelistings"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("activelistings"))


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
        return HttpResponseRedirect(reverse("activelistings"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    form = CreateNewListing()
    if request.method == 'POST':
        form = CreateNewListing(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            bid = form.cleaned_data['bid']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            created_by = request.user
            NewListing.objects.create(title=title, description=description, bid=bid, image=image, category=category,
                                      created_by=created_by)

            return HttpResponseRedirect(reverse("entry", kwargs={'title':title}))


    else:
        return render(request, "auctions/New Listing.html", {'form': form})


def activelistings(request):
    products = NewListing.objects.filter(openbid=True)


    return render(request, 'auctions/activelistings.html', {'products': products})


def entry(request, title):
    item = NewListing.objects.get(title=title)
    bids = Bid.objects.filter(title=item)
    current_user=request.user.username
    comm = Comment.objects.filter(title=item)
    max_bid = bids.aggregate(Max('bidValue'))['bidValue__max']
    maxuser=Bid.objects.filter(bidValue=max_bid)
    if item.openbid is False:
        messages.success(
            request, f'Auction for {item} closed!')
        if str(current_user)== str(maxuser[0]):
            messages.success(
                request, f'YOU ARE THE WINNER!!!')
            return render(request, 'auctions/entry.html', {
                'item': item,
                'comm': comm,
                'bids': bids,
                'max_bid': max_bid,
                'maxuser': str(maxuser[0]),
                'current_user': current_user
            })
        else:
            return render(request, 'auctions/entry.html', {
                'item': item,
                'comm': comm,
                'bids': bids,
                'max_bid': max_bid,
                'maxuser': str(maxuser[0]),
                'current_user': current_user
            })



    return render(request, 'auctions/entry.html', {
        'item': item,
        'comm': comm,
        'bids': bids,
        'max_bid': max_bid,

         'current_user':current_user
    })



@login_required
def watchlist(request):
    if request.user.is_authenticated:
        user = request.user.id
        username = request.user.username
        watchlist, created = Watchlist.objects.get_or_create(user_id=user)
        items = watchlist.watchlistitem_set.all()
    else:
        items = []

    context = {'items': items, 'username': username, 'watchlist': watchlist}
    return render(request, 'auctions/watchlist.html', context)


@login_required
def add(request, title):

    user = get_object_or_404(User, username=request.user.username)
    item = NewListing.objects.get(title=title)
    wl = Watchlist.objects.get(user=user)
    myl = WatchlistItem.objects.filter(watchlist=wl)
    for i in myl:
        if str(item) == str(i.product.title):
            return HttpResponse('exist')
    else:
        wo = WatchlistItem.objects.create(product=item, watchlist=wl)

        wo.save()
        watchlist, created = Watchlist.objects.get_or_create(user=user)

        items = watchlist.watchlistitem_set.all()
        username = request.user.username
        context = {'items': items, 'username': username, 'watchlist': watchlist}

        return render(request, 'auctions/watchlist.html', context
                      )


@login_required()
def edit(request, title):
    item = NewListing.objects.get(title=title)
    form = CreateNewListing(instance=item)
    form.fields['title'].widget = forms.HiddenInput()

    form.fields['category'].widget = forms.HiddenInput()
    if request.method == 'POST':
        form = CreateNewListing(request.POST, instance=item)

        if form.is_valid():
            old = NewListing.objects.filter(title=title)

            form.save()
            products = NewListing.objects.all()
            return HttpResponseRedirect(reverse("entry", kwargs={'title':title}))

    context = {'form': form, 'title': title, 'item': item}
    return render(request, 'auctions/edit.html', context
                  )


@login_required
def remove(request, title):
    user = get_object_or_404(User, username=request.user)
    item = NewListing.objects.get(title=title)
    wl = Watchlist.objects.get(user=user)
    myl = WatchlistItem.objects.all()
    for i in myl:
        if str(item) == str(i.product.title):
            WatchlistItem.objects.filter(product=item).delete()
            watchlist, created = Watchlist.objects.get_or_create(user=user)
            items = watchlist.watchlistitem_set.all()
            username = request.user.username
            context = {'items': items, 'username': username, 'watchlist': watchlist}

            return render(request, 'auctions/watchlist.html', context
                          )


@login_required
def addcomment(request, title):
    title = NewListing.objects.get(title=title)
    form = AddComment()
    username = request.user

    if request.method == 'POST':
        form = AddComment(request.POST)
        title = NewListing.objects.get(title=title)
        username = request.user
        if form.is_valid():
            body = form.cleaned_data['body']
            Comment.objects.create(title=title, body=body, username=username)
            messages.success(request, 'The comment is added!')
            return HttpResponseRedirect(reverse('entry', kwargs={'title':title, }))
    else:
        return render(request, "auctions/comment.html", {'form': form, 'title': title})

@login_required
def bid(request, title):
    form = AddBid()
    user = request.user

    if request.method == 'POST':
        form = AddBid(request.POST)

        title = NewListing.objects.get(title=title)
        if form.is_valid():
            bidValue = form.cleaned_data['bidValue']
            bids = Bid.objects.filter(title=title)

            max_bid = bids.aggregate(Max('bidValue'))['bidValue__max']
            if max_bid is None:
                current_bid = title.bid
                if bidValue < current_bid:
                    messages.error(request, 'The bid is too low!')
                    return render(request, 'auctions/bid.html', {'user': user, 'title': title, 'form': form, })
                else:
                    Bid.objects.create(title=title, bidValue=bidValue, user=user)
                    messages.success(request, 'The bid is added!')


                    return HttpResponseRedirect(reverse('entry', kwargs={"title":title}))

            else:
                max_bid = bids.aggregate(Max('bidValue'))['bidValue__max']

                if bidValue <= max_bid:
                    messages.error(request, 'The bid is too low!')
                    return render(request, 'auctions/bid.html', {'user': user, 'title': title, 'form': form,})
                else:
                    Bid.objects.create(title=title, bidValue=bidValue, user=user)
                    messages.success(request, 'The bid is added!')
                    return HttpResponseRedirect(reverse('entry', kwargs={"title":title}))
    else:


         return render(request, 'auctions/bid.html', {'user': user, 'title': title, 'form': form,})

@login_required
def close_bid(request, title):
    item=NewListing.objects.get(title=title)
    if item.openbid==True:
        item.openbid=False
        item.save()

        return HttpResponseRedirect(reverse('entry', kwargs={'title':title, }))


def categories(request):
    categories=Category.objects.all()


    return render(request, 'auctions/categories.html', {  'categories':categories})

def category(request, title):

    items=NewListing.objects.filter(category=title, openbid=True)

    return render(request, 'auctions/categories.html', {  'items':items, 'title':title})

def test(request):
    messages='YOU WINNER'
    HttpResponseRedirect(reverse('test', kwargs={'messages':messages}))
