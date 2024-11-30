from django.contrib.auth.models import User
from django.db import models

from events.validators import (
    validate_event_capacity,
    validate_event_dates_and_time,
    validate_event_exists,
    validate_google_map_link,
    validate_total_participants,
)


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    total_participants = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(default="00:00:00")
    end_time = models.TimeField(default="00:00:00")
    banner = models.ImageField(upload_to="event_banners/")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "List"
        verbose_name_plural = "Lists"

    def clean(self):
        validate_total_participants(self)
        validate_event_dates_and_time(self)

    def __str__(self):
        return str(self.title)


class EventSignup(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_active": True}, db_index=True
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, limit_choices_to={"is_verified": True}, db_index=True
    )
    signup_date = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ("user", "event")
        ordering = ["signup_date"]
        verbose_name = "Registration"
        verbose_name_plural = "Registrations"

    def clean(self):
        validate_event_exists(self)
        validate_event_capacity(self)

    def __str__(self):
        return str(self.event.title)


class Location(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="location")
    address = models.CharField(max_length=255)
    google_map_link = models.URLField(max_length=500)

    def clean(self):
        validate_google_map_link(self)

    def __str__(self):
        return self.address
