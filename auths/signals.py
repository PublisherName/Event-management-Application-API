from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.tokens import get_token_generator

from auths.models import UserActivationToken
from preferences.enums import EmailTemplateType
from preferences.models import EmailTemplate
from root.tasks import send_email_task


@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):
    reset_password_template = EmailTemplate.get_email_template_by_type(
        EmailTemplateType.USER_RESET_PASSWORD
    )
    if not reset_password_template:
        raise ValueError("Password reset email template not found")

    email_title = reset_password_template.subject
    email_template = {
        "html": reset_password_template.body_html,
        "plaintext": reset_password_template.body_plaintext,
    }

    context = {
        "first_name": reset_password_token.user.first_name,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "reset_password_token": reset_password_token.key,
    }

    send_email_task.delay(
        email_template,
        reset_password_token.user.email,
        email_title,
        context,
    )


@receiver(post_save, sender=User)
def send_activation_email(instance, created, **kwargs):
    if created and not instance.is_active:
        activation_template = EmailTemplate.get_email_template_by_type(
            EmailTemplateType.ACCOUNT_ACTIVATION
        )

        if not activation_template:
            raise ValueError("Account activation email template not found")

        token = get_token_generator().generate_token(instance)
        UserActivationToken.objects.create(user=instance, token=token).save()

        activation_link = (
            f"{settings.FRONTEND_URL}/activate/"
            f"{urlencode({'email': instance.email})}/"
            f"{urlencode({'token': token})}"
        )

        context = {
            "username": instance.username,
            "token": token,
            "activation_link": activation_link,
        }

        email_title = activation_template.subject
        email_template = {
            "html": activation_template.body_html,
            "plaintext": activation_template.body_plaintext,
        }
        send_email_task.delay(email_template, instance.email, email_title, context)
