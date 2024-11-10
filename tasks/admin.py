from django.contrib import admin

from .models import Task, Metric

admin.site.register(Task)
admin.site.register(Metric)
