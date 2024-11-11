import datetime
from unittest.mock import patch

import pytest
from django.http import HttpResponse
from django.test import RequestFactory

from tasks.models import Task
from tasks.views import (create_task, error_404_view, get_all_tasks,
                         get_task_by_id)


@pytest.mark.django_db
class TestViews:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.factory = RequestFactory()

        task1 = Task(
            start_date=datetime.datetime(2020, 1, 1),
            end_date=datetime.datetime(2020, 1, 5),
        )
        task2 = Task(
            start_date=datetime.datetime(2020, 1, 3),
            end_date=datetime.datetime(2020, 1, 7),
        )
        tasks = [task1, task2]

        Task.objects.bulk_create(tasks)

    @patch("tasks.tasks.calculate_average_cycle_time.delay")
    def test_create_task_view(self, mock_task=None):
        form_data = {
            "task_name": "Test Task",
            "start_date": "2020-01-01:00:00",
            "end_date": "2020-01-05:00:00",
        }
        request = self.factory.post("/create/", data=form_data)

        response: HttpResponse = create_task(request)
        assert response.status_code == 302
        mock_task.assert_called_once()

    def test_get_all_tasks_view(self):
        request = self.factory.get("/tasks/")
        response: HttpResponse = get_all_tasks(request)
        assert response.status_code == 200

    def test_get_task_by_id_view(self):
        request = self.factory.get("/tasks/1")
        response: HttpResponse = get_task_by_id(request, 1)
        assert response.status_code == 200

    def test_error_404_view(self):
        request = self.factory.get("/blah-fake-url/")
        response: HttpResponse = error_404_view(request, Exception)
        assert response.status_code == 404
