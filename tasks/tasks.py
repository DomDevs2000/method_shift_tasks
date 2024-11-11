from celery import shared_task

from .models import Metric, Task


@shared_task
def calculate_average_cycle_time() -> float:
    tasks: Task = Task.objects.all()
    average_cycle_time: float = Task.average_cycle_time(list(tasks))
    Metric.update_average_cycle_time(average_cycle_time)

    return average_cycle_time
