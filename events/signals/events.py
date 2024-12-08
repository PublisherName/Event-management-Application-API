from django.core.exceptions import PermissionDenied
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from events.models.event import Event


@receiver(pre_delete, sender=Event)
def restrict_event_deletion(instance, **kwargs):
    """
    Restrict the deletion of an event if the user is not the creator or a superuser.
    """

    request = kwargs.get("request")
    if request:
        user = request.user
        if not (user == instance.created_by or user.is_superuser):
            raise PermissionDenied("You do not have permission to delete this event.")


@receiver(pre_save, sender=Event)
def validate_event(instance, **kwargs):
    """
    Validate the event instance before saving it to the database.
    """

    instance.full_clean()
