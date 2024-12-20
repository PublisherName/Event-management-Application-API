from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils import timezone
from django.utils.timezone import make_aware

from events.enums.status import EventStatus


def validate_event_dates_and_time(instance):
    now = timezone.now()

    if all([instance.start_date, instance.start_time, instance.end_date, instance.end_time]):
        start_datetime = datetime.combine(instance.start_date, instance.start_time)
        start_datetime = make_aware(start_datetime)

        end_datetime = datetime.combine(instance.end_date, instance.end_time)
        end_datetime = make_aware(end_datetime)

        # Validate that start datetime is in the future
        if start_datetime <= now:
            raise ValidationError(
                {
                    "start_date": ("The start date must be in the future."),
                    "start_time": ("The start time must be in the future"),
                }
            )

        # Validate that end datetime is greater than start datetime
        if end_datetime <= start_datetime:
            raise ValidationError(
                {
                    "end_date": ("The end date must be greater or equal to start date."),
                    "end_time": ("The end time must be greater than start time."),
                }
            )


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

    if not instance.event.status == EventStatus.ACTIVE:
        raise ValidationError({"event": "Event is not active."})


def validate_event_capacity(instance):
    if instance.event.total_participants <= instance.event.eventsignup_set.count():
        raise ValidationError(
            {"event": f"The event '{instance.event.title}' has reached the maximum quotas."}
        )


def validate_google_map_link(instance):
    url_validator = URLValidator()
    try:
        url_validator(instance.google_map_link)
    except ValidationError:
        raise ValidationError({"google_map_link": "Invalid URL format."})


def validate_event_attributes(instance, context):
    required_attributes = [
        "location",
        "schedule",
        "banner",
    ]
    if context == "status":
        event_instance = instance
    elif context == "event":
        event_instance = instance.event
    else:
        return

    if (
        context == "status" and instance.status in [EventStatus.ACTIVE, EventStatus.COMPLETED]
    ) or context == "event":
        missing_attributes = []
        for attr in required_attributes:
            if attr == "banner":
                if not event_instance.pk or not event_instance.banner.exists():
                    missing_attributes.append("banner")
            else:
                if not getattr(event_instance, attr, None):
                    missing_attributes.append(attr)

        if missing_attributes:
            raise ValidationError(
                {
                    context: (
                        f"The event must have the following attributes: "
                        f"{', '.join(missing_attributes)}."
                    )
                }
            )
