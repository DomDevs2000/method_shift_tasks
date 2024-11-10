from celery import shared_task
from .models import Task, Metric

@shared_task
def calculate_average_cycle_time()-> float:
    tasks: Task = Task.objects.all()
    average_cycle_time: float = Task.average_cycle_time(tasks) 
    Metric.update_average_cycle_time(average_cycle_time)

    return average_cycle_time
