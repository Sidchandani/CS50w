from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.core.exceptions import ValidationError
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def  show(request,title):
    return render( request, "encyclopedia/show.html", {
        'title':title,
        'entry':util.get_entry(title)
    })

def search(request):
    res=[]
    query= request.GET.get('q')
    entries= util.list_entries()
    for entry in entries:
        if query.lower()==entry.lower() :
            return show(request,entry)
        elif query.lower() in entry.lower():
            res.append(entry)
    else:
        if len(res)>0:
            return render(request,"encyclopedia/search.html", { "res":res })
        else:
            return HttpResponse("<h1>Error 404 : NOT Found</h1>")


def func(x):
    if x in util.list_entries():
        raise ValidationError("** Title Already Exists! **")
    else:
        return x

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title",validators=[func] )
    content = forms.CharField(widget=forms.Textarea(attrs={'style':'height:80vh;'}))

def create(request):
    if request.method == "POST":
        # if req is POST then get info. becz POST req. is done on FORM submission
        form = NewEntryForm(request.POST)
        print(form)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            util.save_entry(title, content)
            return show(request,title)
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    else:
        # else req. is GET so, show them a blank form
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm()
        })

def edit(request,title):
    if request.method == "POST":
        content = request.POST.get('content')
        util.save_entry(title, content)
        return show(request,title)

    content=util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
                "title":title,
                "content":content
            })

def random(request):
    return show(request,choice(util.list_entries()))