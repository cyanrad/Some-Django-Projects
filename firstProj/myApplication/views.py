from django.shortcuts import render
from django.http import HttpResponse

from . import dayCheck


def index(request):
    return render(request, "myApplication/index.html", {
        "color": "black"
    })


def color(request, name):
    return render(request, "myApplication/index.html", {
        "color": name
    })


def birthday(request):
    text = ""
    myColor = ""
    if(dayCheck.isRadwansBirthDay()):
        text = "It is Radwan's Birthday :)"
        myColor = "green"
    else:
        text = "It is NOT Radwan's Birthday :("
        myColor = "red"
    print("test")

    return render(request, "myApplication/BD.html", {
        "text": text,
        "color": myColor
    })
