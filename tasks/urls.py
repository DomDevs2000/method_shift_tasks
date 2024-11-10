from django.urls import path

from . import views 

urlpatterns = [
    path('', views.get_all_tasks, name='get_all_tasks'),
    path('create/', views.create_task, name='create_task'),
    path('<int:pk>/', views.get_task_by_id, name='task_by_id'),
]
