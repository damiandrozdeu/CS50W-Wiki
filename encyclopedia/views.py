from django.shortcuts import render
from markdown2 import markdown
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
import random

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'my-title-class'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class': 'my-content-class'}))


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, name):
    allentries = util.list_entries()
    if name in allentries:
        formated_text = markdown(util.get_entry(name))
        return render(request, "encyclopedia/entry.html", {
            "entries": formated_text,
            "title": name
        })
    else:
        return render(request, "encyclopedia/error_new_page.html", {
            "title": name
        })


def newpage(request):
    if request.method == "POST":
        allentries = util.list_entries()
        title = request.POST.get('title')
        content = request.POST.get('content')
        print(title)
        print(allentries)
        if title in allentries:
            return render(request, "encyclopedia/error.html",
                   {
                       "title": title
                   })
        else:       
            util.save_entry(title=title, content=content) 
        return redirect("title", name=title)
    return render(request, "encyclopedia/new_page.html", {
        "form": NewTaskForm()
    })

def search(request):
    if request.method == "POST":
        allentries = util.list_entries()
        searched = []
        title = request.POST.get("q")
        if title in allentries:
            formated_text = markdown(util.get_entry(title))
            return render(request, "encyclopedia/entry.html", {
            "entries": formated_text,
            "title":title }
            )
        else:
            for entry in allentries:
                if title.lower() in entry.lower():
                    searched.append(entry)
            return render(request,"encyclopedia/search.html", {
            "entries": searched }
            )

def random_page(request):
    choice = random.choice(util.list_entries())
    formated_text = markdown(util.get_entry(choice))
    return render(request, "encyclopedia/entry.html", {
        "entries": formated_text,
        "title": choice
    })

def edit(request, name):
    raw_text = util.get_entry(name).replace('\r\n', '\n')
    inital_data = {
        "title": name,
        "content": raw_text
    }
    form = NewTaskForm(initial=inital_data)
    if request.method == "POST":
        updated_name = request.POST.get("title")
        updated_raw_text = request.POST.get("content")
        util.save_entry(title=updated_name, content=updated_raw_text)
        return redirect("title", name=name)

    return render(request, "encyclopedia/edit.html", {
        "title": name,
        "form": form
    })

