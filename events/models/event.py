from django.contrib.auth.models import User
from django.db import models

from events.enums.status import EventStatus
from events.validators import (
    validate_event_attributes,
    validate_total_participants,
)


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        limit_choices_to={"is_active": True},
    )
    total_participants = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=EventStatus.choices,
        default=EventStatus.DRAFT,
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Event"
        verbose_name_plural = "Event"

    def clean(self):
        validate_total_participants(self)
        validate_event_attributes(self, "status")

    def __str__(self):
        return f"Event: {self.title}"
