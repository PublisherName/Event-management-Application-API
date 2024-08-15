from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task(name="send_email_task")
def send_email_task(email_template, user_email, email_title, context):
    email_html_message = render_to_string(email_template["html"], context)
    email_plaintext_message = render_to_string(email_template["plaintext"], context)
    try:
        msg = EmailMultiAlternatives(
            email_title,
            email_plaintext_message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
        return {"status": "success", "message": f"Email sent to {user_email}"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}
