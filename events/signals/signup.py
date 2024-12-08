from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from events.models.signup import EventSignup
from preferences.enums import EmailTemplateType
from preferences.models import EmailTemplate
from root.tasks import send_email_task


@receiver(post_save, sender=EventSignup)
def send_event_registration_email(instance, created, **kwargs):
    """
    Send an email to the user after successfully signing up for an event.
    """

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
    """
    Validate the eventsignup instance before saving it to the database.
    """

    instance.full_clean()
