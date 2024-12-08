from django.contrib.auth.models import User
from django.db import models

from events.enums.status import EventStatus
from events.models.event import Event
from events.validators import (
    validate_event_attributes,
    validate_event_capacity,
    validate_event_exists,
)


class EventSignup(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_active": True}, db_index=True
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        limit_choices_to={"status": EventStatus.ACTIVE},
        db_index=True,
    )
    signup_date = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ("user", "event")
        ordering = ["signup_date"]
        verbose_name = "Attendee"
        verbose_name_plural = "Attendee"

    def clean(self):
        validate_event_exists(self)
        validate_event_attributes(self, "event")
        validate_event_capacity(self)

    def __str__(self):
        return f"{self.user.username} has signed up for {self.event.title} event."
