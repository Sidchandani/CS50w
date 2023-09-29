from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse

from .models import User,Product,Bid,Comment


def index(request):
    products=Product.objects.all()
    return render(request, "auctions/index.html",{"products":products,'heading':"Active Listings"})


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

def create(request):
    if request.method == 'POST':
        title = request.POST["title"]
        category = request.POST["category"]
        price = request.POST["price"]
        desc = request.POST["desc"]
        image = request.POST["image"]

        p=Product(product_name=title,created_by=request.user.username,category=category,price=price,desc=desc,image=image)
        p.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request,"auctions/create.html")

def close_view(request,id):
    if request.method == 'POST':
        prod=Product.objects.get(pk=id)
        prod.closed=True
        prod.winner=request.POST["winner"]
        prod.save()

    return render(request, 'auctions/close.html',{'winner':prod.winner})

def quick_view(request,id):
    if request.method == 'POST':
        placed_bid = float(request.POST["placed_bid"])
        prod=Product.objects.get(product_id=id)
        b=prod.bid.all()
        if prod.closed:
            return close_view(request,prod.product_id)
        
        # Proccess to fetch watchlist title
        User=request.user
        if len(prod.user.filter(username=User.username)):
            wl_status='Remove From Watchlist'
        else:
            wl_status='Add To Watchlist'

        # show close button becz a bid is already exists
        if User.username==prod.created_by:
            close=True
        else:
            close=False

        try:
            b=b[0]

            if placed_bid>b.highest:
                b.highest=placed_bid
                b.cnt+=1
                b.user=User
            else:
                return render(request, "auctions/quick_view.html",{'product':prod,'bid':b,'message':True,'wl_status':wl_status,'close':close})
        except:
            if placed_bid>prod.price:
                b=Bid(prod=prod,highest=placed_bid,cnt=1,user=User)
            else:
                # bid doesn't exists already & the one we were trying to place, doesn't qualify so remove close button As NO BID IS PLACED
                close=False
                return render(request, "auctions/quick_view.html",{'product':prod,'bid':b,'message':True,'wl_status':wl_status,'close':close})
        b.save()
        return render(request, "auctions/index.html",{'message':'Your Bid was Successfully Placed.','products':Product.objects.all(),'heading':"Active Listings"})

    prod=Product.objects.get(product_id=id)
    # if a prod is closed redirect it to closed page..
    if prod.closed:
        return render(request, 'auctions/close.html',{'winner':prod.winner})
        
    User=request.user
    b=prod.bid.all()
    try:
        b=b[0]
        # if bid is placed then user can have close button
        if User.username==prod.created_by:
            close=True
        else:
            close=False
    except:
        close=False

    # Proccess to fetch watchlist title
    if len(prod.user.filter(username=User.username)):
        wl_status='Remove From Watchlist'
    else:
        wl_status='Add To Watchlist'

    # comments 
    all_comm=prod.comment.all()

    return render(request, "auctions/quick_view.html",{'product':prod,'bid':b,'wl_status':wl_status,'close':close,'all_comm':all_comm})

def watchlist(request):
    if request.method == 'POST':
        prod=Product.objects.get(pk=int(request.POST["id"]))
        User=request.user
        if len(prod.user.filter(username=User.username)):
            User.WatchList.remove(prod)
        else:
            User.WatchList.add(prod)
    return render(request, "auctions/index.html",{'products':request.user.WatchList.all(),'heading':"Your WatchList"})

def post_comm(request,id):
    if request.method == 'POST':
        Prod=Product.objects.get(pk=id)
        User=request.user
        comm=request.POST["cmt"]
        C=Comment(comm=comm,user=User)
        C.save()
        C.prod.add(Prod)

    return redirect('quick_view',id=id)

def categories(request):
    cats=[]
    prods=Product.objects.all()
    for prod in prods:
        if prod.category not in cats:
            cats.append(prod.category)
    return render(request,'auctions/categories.html',{'cats':cats})

def show_cat(request,cat):
    all_prods=Product.objects.all()
    prods=all_prods.filter(category=cat)
    heading="Category: "+cat
    return render(request, "auctions/index.html",{"products":prods,'heading':heading})
