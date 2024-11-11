from django.contrib import admin

from .models import Metric, Task

admin.site.register(Task)
admin.site.register(Metric)
