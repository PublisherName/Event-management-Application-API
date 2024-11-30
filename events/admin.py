from django.contrib import admin
from django.db.models import Q

from root.base_admin import SummernoteModelAdmin  # type: ignore

from .models import Event, EventSignup, Location


class LocationInline(admin.StackedInline):
    model = Location
    extra = 0


@admin.register(Event)
class EventAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    list_display = (
        "title",
        "start_date",
        "end_date",
        "start_time",
        "end_time",
        "total_participants",
        "formatted_created_at",
        "is_verified",
    )
    search_fields = ("title", "description", "location")
    list_filter = ("start_date", "end_date", "created_at", "updated_at", "is_verified")
    readonly_fields = ["created_by"]
    inlines = [LocationInline]

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


@admin.register(EventSignup)
class EventSignupAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "signup_date")
    search_fields = ("user", "event", "signup_date")
    list_filter = (
        "event",
        "signup_date",
    )
    readonly_fields = ["signup_date"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("address", "google_map_link")
    search_fields = ("address", "google_map_link")
    list_filter = ("address",)
