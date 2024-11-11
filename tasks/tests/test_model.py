from datetime import date, datetime, timedelta

import pytest
from _pytest.python_api import approx
from django.core.exceptions import ValidationError

from tasks.models import Task


@pytest.mark.django_db
class TestTaskModel:
    def test_cycle_time(self):
        task = Task(start_date=date(2020, 1, 1), end_date=date(2020, 1, 5))
        assert task.cycle_time == "4 days, 0 hours"

    def test_clean_raises_validation_error(self):
        task = Task(start_date=date(2020, 1, 5), end_date=date(2020, 1, 4))
        with pytest.raises(ValidationError):
            task.clean()

    def test_average_cycle_time(self):
        task1: Task = Task(start_date=date(2020, 1, 1), end_date=date(2020, 1, 5))
        task2: Task = Task(start_date=date(2020, 1, 3), end_date=date(2020, 1, 10))
        tasks: list[Task] = [task1, task2]
        assert Task.average_cycle_time(tasks) == 5.5
