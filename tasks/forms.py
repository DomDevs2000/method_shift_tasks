
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Task
        fields = ['task_name', 'start_date', 'end_date']
