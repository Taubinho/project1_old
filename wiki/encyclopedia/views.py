import random
import pdb

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms



from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def edit(request, name):

    if request.method == 'POST':
        form = New_page_form(request.POST)
        form.fields["title"].required = False
        pdb.set_trace()
        if form.is_valid():
            title = name
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
        else:
            errors = form.errors
        return HttpResponseRedirect(reverse("entry", args=[name]))

    else:
        content = util.get_entry(name)
        initial_data = {"title":name, "content": content}
        form = New_page_form(initial=initial_data)    
        form.fields['title'].widget.attrs['disabled'] = True
        return render(request, "encyclopedia/edit.html", {"form": form,
                                                        "title": name})

def entry(request, name):

    content = util.get_entry(name)

    if not content:
        return render(request, "encyclopedia/error.html", {"error": name})

    return render(request, "encyclopedia/entry.html", {"content": content, "title": name})


def new_page(request):

    if request.method == "POST":

        form = New_page_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {"error": title})
            
            else:
                util.save_entry(title, content)


        return HttpResponseRedirect(reverse("index"))
    return render(request, "encyclopedia/new_page.html", {"form": New_page_form()})

def random_entry(request):

    ran_entry = random.choice(util.list_entries())

    return render(request, "encyclopedia/entry.html", {"content": util.get_entry(ran_entry), "title": ran_entry})

def search(request):
    term = request.GET.get("q")

    if util.get_entry(term):
        return render(request, "encyclopedia/entry.html", {"content": util.get_entry(term), "title": term})
    
    results = util.search_entries(term)

    return render(request, "encyclopedia/search.html", {"term": term,
                                                        "results": results})

class New_page_form(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea, label="content")