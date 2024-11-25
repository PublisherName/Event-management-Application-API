from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.tokens import get_token_generator

from auths.models import UserToken
from root.tasks import send_email_task


@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):
    email_title = f"Password Reset for {settings.PROJECT_TITLE}"
    email_template = {
        "html": "email/user/user_reset_password.html",
        "plaintext": "email/user/user_reset_password.txt",
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
        token = get_token_generator().generate_token(instance)
        UserToken.objects.create(user=instance, token=token).save()

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

        email_title = f"Account activation for {settings.PROJECT_TITLE}"
        email_template = {
            "html": "email/user/acc_active_email.html",
            "plaintext": "email/user/acc_active_email.txt",
        }
        send_email_task.delay(email_template, instance.email, email_title, context)
