from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_event_dates(start_date, end_date):
    if start_date and start_date <= timezone.now():
        raise ValidationError("The start date must be in the future.")
    if end_date and end_date <= start_date:
        raise ValidationError("The end date must be after the start date.")


def validate_total_participants(total_participants):
    if total_participants <= 0:
        raise ValidationError("Total participants must be greater than 0.")
