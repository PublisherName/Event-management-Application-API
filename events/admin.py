from django.contrib import admin
from django.db.models import Q

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "formatted_start_date",
        "formatted_end_date",
        "total_participants",
        "formatted_created_at",
        "is_verified",
    )
    search_fields = ("title", "description", "location")
    list_filter = ("start_date", "end_date", "created_at", "updated_at", "is_verified")
    readonly_fields = ["created_by"]

    @staticmethod
    def formatted_start_date(obj):
        return obj.start_date.strftime("%Y-%m-%d")

    formatted_start_date.short_description = "Start Date"

    @staticmethod
    def formatted_end_date(obj):
        return obj.end_date.strftime("%Y-%m-%d")

    formatted_end_date.short_description = "End Date"

    @staticmethod
    def formatted_created_at(obj):
        return obj.created_at.strftime("%Y-%m-%d")

    formatted_created_at.short_description = "Created At"

    def save_model(self, request, obj, form, change):
        """Assign the current user to the created_by field"""
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Limit the queryset to only show events created by the user"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(created_by=request.user) | Q(is_verified=True))
