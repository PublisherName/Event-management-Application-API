from django.db import models

from events.models.event import Event
from events.validators import validate_event_dates_and_time


class Schedule(models.Model):
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name="schedule",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(default="00:00:00")
    end_time = models.TimeField(default="00:00:00")

    def clean(self):
        validate_event_dates_and_time(self)

    def __str__(self):
        return f"Schedule for {self.event.title}"
