from django.shortcuts import render
from django.http import HttpRequest
from pathlib import Path
from django import forms


class NewTaskForm(forms.Form):
    task = forms.CharField(label='New Task')


def readTaskFile(user):
    fle = Path(f'tasks/tasks_{user}.txt')
    fle.touch(exist_ok=True)
    f = open(fle, mode='r', encoding='utf-8')
    returnList = []
    for line in f:
        returnList.append(line)

    f.close()
    return returnList


def appendToFile(user, data):
    f = open(f'tasks/tasks_{user}.txt', mode='a', encoding='utf-8')
    f.write('\n'+data)
    f.close()


def loadTasks(request, user):
    taskList = readTaskFile(user)
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            taskList.append(task)
            appendToFile(user, task)
            print(task)
        else:  # done so that if there are any form data errors
            return render(request, render(request, "taskManager/tasks.html", {
                "form": form,
                "tasks": taskList,
                "user": user
            }))
    return render(request, "taskManager/tasks.html", {
        "form": NewTaskForm(),
        "tasks": taskList,
        "user": user
    })


def index(request):
    return render(request, "taskManager/index.html")
