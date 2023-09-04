import random
import pdb

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from markdown2 import markdown



from . import util


def index(request):
    """
    Landing page for the app lists all the Wiki entries
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def edit(request, name):
    """
    Gives the site the ability to edit the entries
    """

    # if the request method is POST the user must have provided the needed information to edit the entry
    if request.method == 'POST':

        # the form containing the needed information
        form = New_page_form(request.POST)

        # we disable the title field requirement so the form can passs its validation
        # the form on the edit page has this field disabled, so te user should be able to edit only the entry they are on 
        form.fields["title"].required = False

        # if the form is valid we proceed and save the new data and redirrct the user to the now edited entry page
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(name, content)
        return HttpResponseRedirect(reverse("entry", args=[name]))

    # if the request method is GET we must render the edit page for the entry wanted by the user
    else:

        # we must get the content of the entry the user requested so we can pre-populate the form we will use for the editing
        content = util.get_entry(name)

        # the initial data variable that stores the content of the entry pre-edit
        initial_data = {"title":name, "content": content}

        # we initialize the New_page_form, with the data of the entry
        form = New_page_form(initial=initial_data)

        # we disable the forms title input so the user cannot change it    
        form.fields['title'].widget.attrs['disabled'] = True

        # we render the edit page
        return render(request, "encyclopedia/edit.html", {"form": form,
                                                        "title": name})

def entry(request, name):
    """
    Renders the page for each entry if it exists
    """

    # get the content of the entry the user wanted
    content = util.get_entry(name)

    # if it does not exist we show the user the error of his ways
    if not content:
        return render(request, "encyclopedia/error.html", {"not_found": name})
    
    # else we render the desired entry
    return render(request, "encyclopedia/entry.html", {"content": util.markdown_lite(content), "title": name})


def new_page(request):
    """
    Implements the ability to create new entries for our Wiki
    """

    # if we get a here using a POST method we must have gotten data from the user for a new entry
    if request.method == "POST":

        # a from containing the dato for new entry
        form = New_page_form(request.POST)

        # checks the validness of the form
        if form.is_valid():

            # we save the data needed to create a new entry, specifically the title for the entry and its content
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # if the entry with the same title already exists we show user the error page
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {"error": title})
            
            # else we save the entry 
            else:
                util.save_entry(title, content)

        # after a new entry is saved we redirect the user to the index page
        return HttpResponseRedirect(reverse("index"))
    
    # if the method was not POST (so it was GET), we render the new_page.html which contains the form (New_page_form) where 
    # the user can input the information for a new entry
    else:
        return render(request, "encyclopedia/new_page.html", {"form": New_page_form()})

def random_entry(request):
    """
    Takes the user to a random entry page among the entries saved
    """


    ran_entry = random.choice(util.list_entries())

    return render(request, "encyclopedia/entry.html", {"content": util.markdown_lite(util.get_entry(ran_entry)), "title": ran_entry})

def search(request):
    """
    Implements the search function on the site, whereby we redirect the user to the site for the 
    entry they searched, if the search function doesn't return an exact match we show a list of list of all encyclopedia 
    entries that have the query as a substring. For example, if the search query were ytho, then Python should appear in the 
    search results.
    """

    term = request.GET.get("q")

    # if the search term returns a direct result we render the requested entry
    if util.get_entry(term):
        return render(request, "encyclopedia/entry.html", {"content": util.get_entry(term), "title": term})
    
    # if not then we use the search_entries function to return a list of all entries that have the query as substring
    results = util.search_entries(term)

    # we render the search page with the results returned from the search_entries function
    return render(request, "encyclopedia/search.html", {"term": term,
                                                        "results": results})


"""
Class for the form object we use on the new_page and edit pages, it has two
input fields.
"""
class New_page_form(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea, label="content")