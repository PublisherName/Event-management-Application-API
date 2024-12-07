from django.db import models

from events.models.event import Event
from events.validators import validate_google_map_link


class Location(models.Model):
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name="location",
    )
    address = models.CharField(max_length=255)
    google_map_link = models.URLField(max_length=500)

    def clean(self):
        validate_google_map_link(self)

    def __str__(self):
        return self.address
