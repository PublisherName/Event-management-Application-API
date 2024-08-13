from django.contrib.auth.models import User
from django.db import models

from events.validators import (
    validate_event_capacity,
    validate_event_dates_and_time,
    validate_event_exists,
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
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    banner = models.ImageField(upload_to="event_banners/")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "List"
        verbose_name_plural = "Lists"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_banner = self.banner

    @property
    def old_banner(self):
        return self._old_banner

    @old_banner.setter
    def old_banner(self, value):
        self._old_banner = value

    def clean(self):
        super().clean()
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

    def clean(self) -> None:
        validate_event_exists(self.event)
        validate_event_capacity(self.event)
        return super().clean()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.event.title)
