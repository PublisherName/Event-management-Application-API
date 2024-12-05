from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import QuerySet


class BannerQuerySet(QuerySet):
    def delete(self, *args, **kwargs):
        """
        Override delete to enforce bulk_delete logic for querysets.
        """
        events_to_check = self.values_list("event_id", flat=True).distinct()
        for event_id in events_to_check:
            total_banners = self.model.objects.filter(event_id=event_id).count()
            banners_to_delete = self.filter(event_id=event_id).count()

            if banners_to_delete >= total_banners:
                verified_event = self.model.objects.filter(
                    event_id=event_id, event__is_verified=True
                ).exists()
                if verified_event:
                    raise PermissionDenied(
                        "Cannot delete banners as it would leave "
                        "a verified event without any banners."
                    )
        super().delete(*args, **kwargs)


class BannerManager(models.Manager):
    def get_queryset(self):
        return BannerQuerySet(self.model, using=self._db)
