from django.core.exceptions import PermissionDenied
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

from events.models import Banner, Event, EventSignup, Location, Schedule
from preferences.enums import EmailTemplateType
from preferences.models import EmailTemplate
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
        event_signup_template = EmailTemplate.get_email_template_by_type(
            EmailTemplateType.EVENT_SIGNUP
        )

        if not event_signup_template:
            raise ValueError("Event signup email template not found")

        email_template = {
            "html": event_signup_template.body_html,
            "plaintext": event_signup_template.body_plaintext,
        }
        email_title = event_signup_template.subject

        context = {
            "user": instance.user.username,
            "event": {
                "title": instance.event.title,
                "start_date": instance.event.schedule.start_date,
                "end_date": instance.event.schedule.end_date,
                "start_time": instance.event.schedule.start_time,
                "end_time": instance.event.schedule.end_time,
                "address": instance.event.location.address,
                "map_link": instance.event.location.google_map_link,
            },
            "current_year": instance.signup_date.year,
        }
        send_email_task.delay(email_template, instance.user.email, email_title, context)


@receiver(pre_save, sender=EventSignup)
def validate_eventSignup(instance, **kwargs):
    """Validate the eventsignup instance before saving it to the database."""
    instance.full_clean()


@receiver(pre_save, sender=Location)
def validate_location(instance, **kwargs):
    """Validate the location instance before saving it to the database."""
    instance.full_clean()


@receiver(pre_save, sender=Schedule)
def validate_schedule(instance, **kwargs):
    """Validate the schedule instance before saving it to the database."""
    instance.full_clean()


@receiver(post_delete, sender=Banner)
@receiver(post_delete, sender=Location)
@receiver(post_delete, sender=Schedule)
def check_verified_event_requirements(instance, **kwargs):
    event = instance.event
    if event:
        has_banner = Banner.objects.filter(event=event).exists()
        has_location = Location.objects.filter(event=event).exists()
        has_schedule = Schedule.objects.filter(event=event).exists()

        if not all([has_banner, has_location, has_schedule]):
            event.is_verified = False
            event.save()


@receiver(pre_delete, sender=Location)
@receiver(pre_delete, sender=Schedule)
def restrict_deletion(instance, **kwargs):
    """Restrict the deletion of a related model if the event is verified."""
    if instance.event.is_verified:
        raise PermissionDenied(
            "You cannot delete this object because its associated with verified event."
        )


@receiver(pre_delete, sender=Banner)
def restrict_banner_deletion(instance, **kwargs):
    """Restrict the deletion of a banner if it is the last one for a verified event."""
    event = instance.event
    if event.is_verified:
        remaining_banners = Banner.objects.filter(event=event).exclude(id=instance.id).count()
        if remaining_banners == 0:
            raise PermissionDenied(
                "You cannot delete this banner because it is the last one "
                "associated with a verified event."
            )
