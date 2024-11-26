from django.db import models

from preferences.enums import EmailTemplateType


class EmailTemplate(models.Model):
    email_type = models.CharField(max_length=50, choices=EmailTemplateType.choices, unique=True)
    subject = models.CharField(max_length=200)
    body_html = models.TextField()
    body_plaintext = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email_type

    @classmethod
    def get_email_template_by_type(cls, email_type):
        try:
            return cls.objects.get(email_type=email_type)
        except cls.DoesNotExist:
            return None
