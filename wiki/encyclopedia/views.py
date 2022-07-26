from ast import Or
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
from . import markdown

import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wikipage(request, title):
    # getting markdown data
    entry = util.get_entry(title)
    if entry is not None:
        return render(request, f"encyclopedia/wikipage.html", {
            "title": title,
            "markdown": markdown.to_markdown(entry)
        })
    else:
        return render(request, "encyclopedia/unknown.html", {
            "title": title
        })


def getRandom(request):
    entryList = util.list_entries()  # getting all existing entries
    entry = random.choice(entryList)
    url = reverse("wikipage", kwargs={'title': entry})
    return HttpResponseRedirect(url)


# >> modifies page submit request handler
# >> @ entry is None: create entry
def edit(request, title):
    # if the request was not a POST
    if request.method == "POST":
        entryContent = request.POST["page_content"]
        util.save_entry(title, entryContent)

        url = reverse("wikipage", kwargs={'title': title})
        return HttpResponseRedirect(url)
    else:
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "text": entry,
        })


def create(request):
    # if the request was not a POST
    if request.method == "POST":
        entryContent = request.POST["page_content"]
        title = request.POST["title"]
        if (title in util.list_entries()) or (not title):
            return render(request, "encyclopedia/create.html", {
                "title": title,
                "text": entryContent,
                "title_conflict": True
            })
        util.save_entry(title, entryContent)

        url = reverse("wikipage", kwargs={'title': title})
        return HttpResponseRedirect(url)
    else:
        return render(request, "encyclopedia/create.html", {
            "title": "",
            "text": "",
        })


def search(request):
    # if the request was not a POST
    if not (request.method == "POST"):
        return HttpResponseRedirect(reverse("index"))

    searchItem = request.POST["q"]  # getting the entry to look for
    entryList = util.list_entries()  # getting all existing entries
    # prolly should do that with a db, but eh

    substr_search = []  # list contains all substrings related to the search
    # looping over all entities
    for entry in entryList:

        # if we find a substr
        if entry != None and searchItem in entry:
            if entry == searchItem:  # if we find an exact match
                # redirecting to the wikipage <END>
                url = reverse("wikipage", kwargs={'title': searchItem})
                return HttpResponseRedirect(url)

            else:   # if we get a substring match
                substr_search.append(entry)

    # <END>
    # return the page with substr list
    return render(request, "encyclopedia/search.html", {
        "title": searchItem,
        "entries": substr_search
    })
