from django.core.exceptions import PermissionDenied
from django.db.models.signals import post_delete, pre_delete, pre_save
from django.dispatch import receiver

from events.enums.status import EventStatus
from events.models.banner import Banner
from events.models.location import Location
from events.models.schedule import Schedule


@receiver(pre_save, sender=Schedule)
@receiver(pre_save, sender=Location)
def validate_location(instance, **kwargs):
    """
    Validate the instance before saving it to the database.
    Dont allow changes to a related model if the event is verified.
    """

    if instance.event.status not in [EventStatus.DRAFT]:
        raise PermissionDenied("You can only add objects to draft events.")
    instance.full_clean()


@receiver(pre_delete, sender=Schedule)
@receiver(pre_delete, sender=Location)
def restrict_deletion(instance, **kwargs):
    """
    Restrict the deletion of a related model if the event is verified.
    """

    if instance.event.status not in [EventStatus.DRAFT]:
        raise PermissionDenied("You can only delete objects of a draft event.")


@receiver(post_delete, sender=Banner)
@receiver(post_delete, sender=Location)
@receiver(post_delete, sender=Schedule)
def check_verified_event_requirements(instance, **kwargs):
    """
    Check if the event requirements are met after deleting a related model.
    If the requirements are not met, change the event status to draft.
    """

    event = instance.event
    if event and event.status in [EventStatus.ACTIVE]:
        has_banner = Banner.objects.filter(event=event).exists()
        has_location = Location.objects.filter(event=event).exists()
        has_schedule = Schedule.objects.filter(event=event).exists()

        if not all([has_banner, has_location, has_schedule]):
            event.status = EventStatus.DRAFT
            event.save()
