from django.shortcuts import render
from markdown2 import markdown
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'my-title-class'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class': 'my-content-class'}))


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, name):
    formated_text = markdown(util.get_entry(name))
    return render(request, "encyclopedia/entry.html", {
        "entries": formated_text
    })

def newpage(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title=title, content=content) 
        return HttpResponseRedirect(reverse("index"))
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
            "entries": formated_text }
            )
        else:
            for entry in allentries:
                if title in entry:
                    searched.append(entry)
            return render(request,"encyclopedia/search.html", {
            "entries": searched }
            )


