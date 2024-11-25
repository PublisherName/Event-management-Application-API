from django.core.exceptions import PermissionDenied
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from events.models import Event, EventSignup
from root.tasks import send_email_task


@receiver(pre_delete, sender=Event)
def restrict_event_deletion(instance, **kwargs):
    """Restrict the deletion of an event if the user is not the creator or a superuser."""
    request = kwargs.get("request")
    if request:
        user = request.user
        if not (user == instance.created_by or user.is_superuser):
            raise PermissionDenied("You do not have permission to delete this event.")


@receiver(pre_save, sender=Event)
def validate_event(instance, **kwargs):
    """Validate the event instance before saving it to the database."""
    instance.full_clean()


@receiver(post_save, sender=EventSignup)
def send_event_registration_email(instance, created, **kwargs):
    """Send an email to the user after successfully signing up for an event."""
    if created:
        email_title = f"Event Signup for {instance.event.title}"
        email_template = {
            "html": "email/event/event_signup.html",
            "plaintext": "email/event/event_signup.txt",
        }
        context = {
            "user": instance.user.username,
            "event": {
                "title": instance.event.title,
                "start_date": instance.event.start_date,
                "end_date": instance.event.end_date,
                "start_time": instance.event.start_time,
                "end_time": instance.event.end_time,
                "location": instance.event.location,
                "latitude": instance.event.latitude,
                "longitude": instance.event.longitude,
            },
            "current_year": instance.signup_date.year,
        }
        send_email_task.delay(email_template, instance.user.email, email_title, context)


@receiver(pre_save, sender=EventSignup)
def validate_eventSignup(instance, **kwargs):
    """Validate the eventsignup instance before saving it to the database."""
    instance.full_clean()
