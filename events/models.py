from django.contrib.auth.models import User
from django.db import models

from events.validators import validate_event_dates, validate_total_participants


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    total_participants = models.PositiveIntegerField(validators=[validate_total_participants])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    banner = models.ImageField(upload_to="event_banners/")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

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
        validate_event_dates(self.start_date, self.end_date)

    def __str__(self):
        return str(self.title)
