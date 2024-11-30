from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import make_aware


def validate_event_dates_and_time(instance):
    now = timezone.now()

    if instance.start_date and instance.start_time:
        start_datetime = datetime.combine(instance.start_date, instance.start_time)
        start_datetime = make_aware(start_datetime)
        if start_datetime <= now:
            raise ValidationError(
                {
                    "start_date": ("The start date must be in the future."),
                    "start_time": ("The start time must be in the future"),
                }
            )
    if instance.end_date and instance.end_date <= instance.start_date:
        raise ValidationError({"end_date": ("The end date must be after the start date.")})

    if instance.start_time and instance.end_time and instance.end_time <= instance.start_time:
        raise ValidationError({"end_time": ("The end time must be after the start time.")})


def validate_total_participants(event):
    if event.total_participants is not None and event.total_participants <= 0:
        raise ValidationError({"total_participants": "Total participants must be greater than 0."})

    if event.pk:
        current_signups = event.eventsignup_set.filter().count()
        if event.total_participants < current_signups:
            raise ValidationError(
                {
                    "total_participants": (
                        f"Total participants cannot be less than {current_signups}."
                    )
                }
            )


def validate_event_exists(instance):
    if not instance.event_id:
        raise ValidationError({"event": "Event does not exist."})

    if not instance.event.is_verified:
        raise ValidationError({"event": "Event is not verified."})


def validate_event_capacity(instance):
    if instance.event.total_participants <= instance.event.eventsignup_set.count():
        raise ValidationError(
            {"event": f"The event '{instance.event.title}' has reached the maximum quotas."}
        )
