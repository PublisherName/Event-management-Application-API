import uuid

from django.core.exceptions import PermissionDenied
from django.core.files.storage import default_storage
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from events.models import Event


@receiver(pre_save, sender=Event)
def update_banner_filename(sender, instance, **kwargs):
    """Update the banner filename to a unique name before saving it to the storage."""
    if instance.pk:
        try:
            old_instance = Event.objects.get(pk=instance.pk)
            instance._old_banner = old_instance.banner
        except Event.DoesNotExist:
            instance._old_banner = None
    else:
        instance._old_banner = None

    if instance.banner:
        ext = instance.banner.name.split(".")[-1]
        new_filename = f"{uuid.uuid4()}.{ext}"
        instance.banner.name = default_storage.get_available_name(new_filename)


@receiver(post_save, sender=Event)
def delete_old_banner(sender, instance, **kwargs):
    """Delete the old banner file from the storage when a new banner is uploaded."""
    old_banner = getattr(instance, "_old_banner", None)
    if old_banner and old_banner != instance.banner and default_storage.exists(old_banner.name):
        default_storage.delete(old_banner.name)


@receiver(pre_delete, sender=Event)
def delete_banner_file(sender, instance, **kwargs):
    """Delete the banner file from the storage when an event is deleted."""
    if instance.banner and default_storage.exists(instance.banner.name):
        default_storage.delete(instance.banner.name)


@receiver(pre_delete, sender=Event)
def restrict_event_deletion(sender, instance, **kwargs):
    """Restrict the deletion of an event if the user is not the creator or a superuser."""
    request = kwargs.get("request")
    if request:
        user = request.user
        if not (user == instance.created_by or user.is_superuser):
            raise PermissionDenied("You do not have permission to delete this event.")


@receiver(pre_save, sender=Event)
def validate_event(sender, instance, **kwargs):
    """Validate the event instance before saving it to the database."""
    instance.full_clean()