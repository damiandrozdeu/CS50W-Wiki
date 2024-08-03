from django.shortcuts import render
from markdown2 import markdown

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


