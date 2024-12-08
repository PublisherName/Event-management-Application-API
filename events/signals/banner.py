from django.core.exceptions import PermissionDenied
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from events.enums.status import EventStatus
from events.models.banner import Banner


@receiver(pre_delete, sender=Banner)
def restrict_banner_deletion(instance, **kwargs):
    """
    Restrict the deletion of a banner if it is for a active/completed event.
    """

    if instance.event.status not in [
        EventStatus.DRAFT,
    ]:
        raise PermissionDenied("You can only delete the banner of a draft event.")


@receiver(pre_save, sender=Banner)
def validate_banner(instance, **kwargs):
    """
    Validate the banner instance before saving it to the database.
    Restrict the addition of a banner for a active/completed/cancelled event.
    """

    if instance.event.status not in [
        EventStatus.DRAFT,
    ]:
        raise PermissionDenied("You can only add banners to draft events.")
    instance.full_clean()
