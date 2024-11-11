# Create your views here.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import TaskForm
from .models import Task, Metric
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
    paginator: Paginator = Paginator(tasks, 15)
    page = request.GET.get('page')
    try:
        tasks: Task = paginator.page(page)
    except PageNotAnInteger:
        tasks: Task = paginator.page(1)
    except EmptyPage:
        tasks: Task = paginator.page(paginator.num_pages)

    return render(request, 'all_tasks.html', {'tasks': tasks})


def get_task_by_id(request: HttpRequest, pk: int):
    try:
        task: Task = Task.objects.get(pk=pk)

        return render(request, "task_by_id.html", {"task": task})
    except Task.DoesNotExist:

        return render(request, "404.html", {"error": "No task found"}, status=404)


def display_average_cycle_time(request):
    tasks = Task.objects.all()
    average_cycle_time: float = Task.average_cycle_time(tasks)
    metric = Metric.update_average_cycle_time(average_cycle_time)
    return render(request, 'display_average_cycle_time.html', {'metric': metric})


def error_404_view(request: HttpRequest, exception):
    return render(request, "404.html", status=404)
