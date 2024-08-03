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


