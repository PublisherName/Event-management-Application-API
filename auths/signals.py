from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "reset_password_token": reset_password_token.key,
    }

    # render email text
    email_html_message = render_to_string("email/user/user_reset_password.html", context)
    email_plaintext_message = render_to_string("email/user/user_reset_password.txt", context)

    msg = EmailMultiAlternatives(
        f"Password Reset for {settings.PROJECT_TITLE}",
        email_plaintext_message,
        settings.DEFAULT_FROM_EMAIL,
        [reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
