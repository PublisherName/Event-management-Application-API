from django.db import models


class EmailTemplateType(models.TextChoices):
    EVENT_SIGNUP = "EVENT_SIGNUP", "Event Signup"
    ACCOUNT_ACTIVATION = "ACCOUNT_ACTIVATION", "Account Activation"
    USER_RESET_PASSWORD = "USER_RESET_PASSWORD", "User Reset Password"
