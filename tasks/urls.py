from django.urls import path

from . import views

urlpatterns = [
    path("<int:task_id>/", views.get_task_detail, name="detail"),
    path("", views.get_all_tasks, name="get_all_tasks"),
]
