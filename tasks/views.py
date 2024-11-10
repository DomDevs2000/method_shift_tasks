# Create your views here.
from django.shortcuts import redirect, render

from django.views.decorators.cache import cache_page
from .forms import TaskForm
from .models import Task

from django.http import HttpRequest
def create_task(request: HttpRequest):
    if request.method == "POST":
        form: TaskForm = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("get_all_tasks")
    else:
        form: TaskForm = TaskForm()
    return render(request, "create_task.html", {"form": form})


@cache_page(60*15)
def get_all_tasks(request: HttpRequest):
    tasks: Task = Task.objects.all()
    return render(request, "all_tasks.html", {"tasks": tasks})


def get_task_by_id(request: HttpRequest, pk: int):
    task: Task = Task.objects.get(pk=pk)
    return render(request, "task_by_id.html", {"task": task})
