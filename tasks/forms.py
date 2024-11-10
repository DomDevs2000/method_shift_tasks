
from django import forms
from .models import Tasks

class TaskForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Tasks
        fields = ['task_name', 'start_date', 'end_date']
