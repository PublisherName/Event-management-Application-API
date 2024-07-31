from django import forms
from django.utils import timezone

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "total_participants",
            "start_date",
            "end_date",
            "location",
            "latitude",
            "longitude",
            "banner",
        ]

    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")
        if start_date and start_date <= timezone.now():
            raise forms.ValidationError("The start date must be in the future.")
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        if end_date and start_date and end_date <= start_date:
            raise forms.ValidationError("The end date must be after the start date.")
        return end_date
