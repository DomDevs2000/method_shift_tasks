from datetime import timedelta

from celery import shared_task
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import CharField, DateField, FloatField


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
        total_seconds: float = 0
        task_count: int = tasks.count()

        if task_count == 0:
            return 0

        for task in tasks.all():
            delta: timedelta = task.end_date - task.start_date
            total_seconds += delta.total_seconds()

        average_seconds: float = total_seconds / task_count
        average_delta: timedelta = timedelta(seconds=average_seconds)
        average_days: int = average_delta.days
        average_hours: int = average_delta.seconds // 3600

        return average_days + (average_hours / 24)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date must be after start date.")
        if self.start_date == self.end_date:
            raise ValidationError(
                "Start date and time must be after end date and time."
            )
        return self.end_date

    def __str__(self) -> str:
        return str(self.task_name)


class Metric(models.Model):
    # average_cycle_time: FloatField = models.FloatField()
    name: CharField = models.CharField(max_length=20, null=True, unique=True)
    value = models.FloatField()
    # name: str = models.CharField()

    @classmethod
    def update_average_cycle_time(cls, average_cycle_time):
        try:
            instance = Metric.objects.get(
                name="average_cycle_time",
            )
            instance.value = average_cycle_time
            instance.save(update_fields=["value"])
        except Metric.DoesNotExist:
            instance = Metric.objects.create(
                name="average_cycle_time", value=average_cycle_time
            )
        return instance

    def __str__(self) -> str:
        return str(self.name)
