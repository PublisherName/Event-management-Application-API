from django.db import models

from events.managers.banners import BannerManager
from events.models.event import Event


class Banner(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="banner",
    )
    image = models.ImageField(upload_to="event_banners/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = BannerManager()

    def __str__(self):
        return f"Banner for {self.event.title} uploaded at {self.uploaded_at}"
