# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Tasks
from django.shortcuts import render

def get_task_detail(request, task_id):
    task = Tasks.objects.get(pk=task_id)
    context = {"task": task}
    return render(request, "task/index.html", context)



def get_all_tasks(request):
    tasks = Tasks.objects.all()
    template = loader.get_template("tasks/index.html")
    context = {
        "tasks": tasks,
    }
    return HttpResponse(template.render(context, request))
