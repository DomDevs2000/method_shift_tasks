import datetime

import pytest

from tasks.models import Tasks


@pytest.mark.django_db
def test_cycle_time():
    start_date = datetime.datetime(2022, 1, 1, 12, 0, 0)
    end_date = datetime.datetime(2022, 1, 3, 14, 30, 0)
    task: Tasks = Tasks(task_name="Test Task", start_date=start_date, end_date=end_date)

    assert task.cycle_time == "2 days, 2 hours"
