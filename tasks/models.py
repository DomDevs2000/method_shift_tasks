from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import CharField, DateField


class Task(models.Model):
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

    @classmethod
    def average_cycle_time(cls, tasks) -> float:
        total_seconds = 0
        task_count = tasks.count()

        if task_count == 0:
            return 0

        for task in tasks.all():
            delta: timedelta = task.end_date - task.start_date
            total_seconds += delta.total_seconds()

        average_seconds = total_seconds / task_count
        average_delta = timedelta(seconds=average_seconds)
        average_days = average_delta.days
        average_hours = average_delta.seconds // 3600

        return average_days + (average_hours / 24)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date must be after start date.")
        if self.start_date == self.end_date:
            raise ValidationError("Start date and time must be after end date and time.")
        return self.end_date
    def __str__(self) -> str:
        return str(self.task_name)
