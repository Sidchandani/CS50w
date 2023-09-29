import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User,Post
from django.core.paginator import Paginator

def index(request):
    p=Post.objects.order_by("-timestamp").all()
    if request.user.is_authenticated:
        for post in p:
            if post in request.user.liked.all():
                post.is_liked=True

    posts=[post.serialize() for post in p]

    # Show 10 posts per page.
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{'heading':'All Posts',"page_obj": page_obj})


def following(request):
    users=request.user.followings.all()
    p=Post.objects.order_by("-timestamp").all()
    posts=[]
    for post in p:
        u=User.objects.get(username=post.user)
        if u in users:
            posts.append(post)

    if request.user.is_authenticated:
        for post in posts:
            if post in request.user.liked.all():
                post.is_liked=True       
    
    # Show 10 posts per page.
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{'heading':'Following',"page_obj": page_obj})

def user(request,username):
    user=User.objects.get(username=username)
    followers=user.followers.all()
    posts=user.posts.order_by("-timestamp").all()

    if request.user.is_authenticated:
        for post in posts:
            if post in request.user.liked.all():
                post.is_liked=True

    if request.user in followers:
        msg='Unfollow'
    else:
        msg='Follow'

    # Show 10 posts per page.
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request,'network/user.html',{'user':user,'page_obj':page_obj,
            'followers':len(followers),'followings':len(user.followings.all()),
            'flw':msg})


# APIs

@csrf_exempt
@login_required
def post(request):
        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
        data = json.loads(request.body)
        user=data['user']
        p=Post(user=user,body=data['body'])
        p.save()
        u=User.objects.get(username=user)
        u.posts.add(p)
        u.save()
    
        return JsonResponse({"message": "Posted successfully."}, status=201)


@csrf_exempt
@login_required
def edit(request, postid):
        if request.method != "PUT":
            return JsonResponse({"error": "PUT request required."}, status=400)
        else:
            data = json.loads(request.body)
            post=Post.objects.get(id=postid)
            if data.get('body') is not None:
                post.body=data['body']
            if data.get('like_status') is not None:
                like_status=data['like_status']
                u=User.objects.get(username=data['usr'])
                if like_status == 'like':
                    post.likes += 1
                    u.liked.add(post)
                else:
                    post.likes -= 1
                    u.liked.remove(post)
                u.save()
                
            post.save()
            return JsonResponse({"message": "Post Changed successfully."}, status=201)


@csrf_exempt
@login_required
def follow(request, status):
        if request.method != "PUT":
            return JsonResponse({"error": "PUT request required."}, status=400)
        else:
            data = json.loads(request.body)
            main=User.objects.get(username=data['main'])
            follower=User.objects.get(username=data['follower'])
            if status=='Follow':
                main.followers.add(follower)
                follower.followings.add(main)
            else:
                main.followers.remove(follower)
                follower.followings.remove(main)
            main.save()
            follower.save()
            
            return JsonResponse({"message": "Post Edited successfully."}, status=201)




# Login system

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
