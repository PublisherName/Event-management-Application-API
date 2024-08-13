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
            raise ValidationError("The start date and time must be in the future.")

    if instance.end_date and instance.end_date <= instance.start_date:
        raise ValidationError("The end date must be after the start date.")

    if instance.start_time and instance.end_time and instance.end_time <= instance.start_time:
        raise ValidationError("The end time must be after the start time.")


def validate_total_participants(event):
    if event.total_participants <= 0:
        raise ValidationError("Total participants must be greater than 0.")

    if event.pk:
        current_signups = event.eventsignup_set.filter().count()
        if event.total_participants < current_signups:
            raise ValidationError(f"Total participants cannot be less than {current_signups}.")


def validate_event_exists(event):
    if not event.is_verified:
        raise ValidationError("Event does not exist or is not verified.")


def validate_event_capacity(event):
    if event.total_participants <= event.eventsignup_set.filter().count():
        raise ValidationError(
            f"The event '{event.title}' has reached the maximum number of participants."
        )
