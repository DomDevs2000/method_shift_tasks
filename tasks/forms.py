from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.TextInput(attrs={"type": "datetime-local"})
    )
    end_date = forms.DateTimeField(
        widget=forms.TextInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Task
        fields = ["task_name", "start_date", "end_date"]

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if end_date < self.cleaned_data['start_date']:
            raise forms.ValidationError("End date must be after start date.")
        return end_date
