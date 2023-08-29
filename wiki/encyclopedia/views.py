import random

from django.shortcuts import render
from django.http import HttpResponse


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):

    content = util.get_entry(name)

    if not content:
        return render(request, "encyclopedia/error.html", {"error": name})

    return render(request, "encyclopedia/entry.html", {"content": content, "title": name})


def new_page(request):
    return render(request, "encyclopedia/new_page.html")

def random_entry(request):

    ran_entry = random.choice(util.list_entries())

    return render(request, "encyclopedia/entry.html", {"content": util.get_entry(ran_entry), "title": ran_entry})

def search(request):
    term = request.GET.get("q")
    results = util.search_entries(term)

    if util.get_entry(term):
        return render(request, "encyclopedia/entry.html", {"content": util.get_entry(term), "title": term})
    
    return render(request, "encyclopedia/search.html", {"term": term,
                                                        "results": results})