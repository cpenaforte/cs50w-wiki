from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

import random

from django.urls import reverse

from . import util

class searchForm(forms.Form):
    search = forms.CharField(label="Search Encyclopedia")

class newPageForm(forms.Form):
    title = forms.CharField(label="Page Title")
    content = forms.CharField(label="Page Content", widget=forms.Textarea, min_length=1)

class editPageForm(forms.Form):
    content = forms.CharField(label="Page Content", widget=forms.Textarea, min_length=1)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry_html(title),
    })

def search(request):
    if request.method == "POST":
        form = searchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            if util.get_entry(search):
                return render(request, "encyclopedia/entry.html", {
                    "title": search,
                    "content": util.get_entry_html(search),
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    "entries": [entry for entry in util.list_entries() if search.lower() in entry.lower()],
                })
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": util.list_entries(),
        })

def create(request):
    if request.method == "POST":
        form = newPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            try :
                util.save_entry(title, content)
            except FileExistsError:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": "Page already exists"
                })
            
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": util.get_entry_html(title),
            })
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form,
                "error": ""
            })
    return render(request, "encyclopedia/create.html", {
        "form": newPageForm(),
        "error": ""
    })

def edit(request, title):
    if request.method == "POST":
        form = editPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            try :
                util.edit_entry(title, content)
            except FileNotFoundError:
                return render(request, "encyclopedia/edit.html", {
                    "form": form,
                    "title": title,
                    "error": "Page not found"
                })
            
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": util.get_entry_html(title),
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "title": title,
                "error": ""
            })
    return render(request, "encyclopedia/edit.html", {
        "form": editPageForm(initial={ "content": util.get_entry(title)}),
        "title": title,
        "error": ""
    })
    
def random_entry(request):
    random_title = random.choice(util.list_entries())
        
    return HttpResponseRedirect(f"wiki/{random_title}")