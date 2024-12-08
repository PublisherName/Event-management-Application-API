from django.core.exceptions import PermissionDenied
from django.db.models.signals import pre_save
from django.dispatch import receiver

from events.enums.status import EventStatus
from events.models.category import Category


@receiver(pre_save, sender=Category)
def restrict_category_update(instance, **kwargs):
    """
    Restrict the update of a category if it is associated with a active/completed event.
    """
    if instance.pk and instance.event_set.exclude(status__in=[EventStatus.DRAFT]).exists():
        raise PermissionDenied("You can only update a category linked to a draft event.")
    instance.full_clean()
