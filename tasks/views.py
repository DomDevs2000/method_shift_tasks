# Create your views here.
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import TaskForm
from .models import Task
from .tasks import calculate_average_cycle_time


def create_task(request: HttpRequest):
    if request.method == "POST":
        form: TaskForm = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            calculate_average_cycle_time.delay()
            return redirect("get_all_tasks")
    else:
        form: TaskForm = TaskForm()
    return render(request, "create_task.html", {"form": form})


def get_all_tasks(request: HttpRequest):
    tasks: Task = Task.objects.all()

    if not tasks:

        return render(request, "404.html", status=404)
    average_cycle = Task.average_cycle_time(tasks)

    return render(
        request, "all_tasks.html", {"tasks": tasks, "average_cycle_time": average_cycle}
    )


def get_task_by_id(request: HttpRequest, pk: int):
    try:
        task: Task = Task.objects.get(pk=pk)

        return render(request, "task_by_id.html", {"task": task})
    except Task.DoesNotExist:

        return render(request, "404.html", {"error": "No task found"}, status=404)


def error_404_view(request: HttpRequest, exception):
    return render(request, "404.html", status=404)
