from django.db import models
from django.db.models.fields import CharField, DateField


class Tasks(models.Model):
    task_name: CharField = models.CharField(max_length=255)
    start_date: DateField = models.DateTimeField()
    end_date: DateField = models.DateTimeField()

    # TODO: Cycle time

    @property
    def cycle_time(self) -> str:
        delta: timedelta = self.end_date - self.start_date
        days: int = delta.days
        hours: int = delta.seconds // 3600
        return f"{days} days, {hours} hours"

    def __str__(self) -> str:
        return str(self.task_name)
