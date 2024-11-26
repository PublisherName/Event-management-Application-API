from django.contrib import admin

from root.base_admin import SummernoteModelAdmin

from .models import EmailTemplate


@admin.register(EmailTemplate)
class EmailTemplateAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    list_display = ("email_type", "subject", "is_active", "updated_at")
    search_fields = ("email_type", "subject")
