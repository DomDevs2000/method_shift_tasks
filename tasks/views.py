# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Tasks


def get_task_detail(request, task_id):
    return HttpResponse("You're looking at Task %s." % task_id)



def get_all_tasks(request):
    tasks = Tasks.objects.all()
    template = loader.get_template("tasks/index.html")
    context = {
        "tasks": tasks,
    }
    return HttpResponse(template.render(context, request))
