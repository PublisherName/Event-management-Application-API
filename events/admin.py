from django.contrib import admin
from django.db.models import Q

from events.filters.category import ActiveCategoryFilter
from root.base_admin import SummernoteModelAdmin  # type: ignore

from .enums import EventStatus
from .models import Banner, Category, Event, EventSignup, Location, Schedule


class LocationInline(admin.StackedInline):
    model = Location
    can_delete = False
    extra = 0


class BannerInline(admin.StackedInline):
    model = Banner
    can_delete = False
    extra = 0


class ScheduleInline(admin.StackedInline):
    model = Schedule
    can_delete = False
    extra = 0


@admin.register(Event)
class EventAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "total_participants",
        "formatted_created_at",
        "status",
    )
    search_fields = (
        "title",
        "description",
        "status",
        "category__name",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "status",
        ActiveCategoryFilter,
    )
    readonly_fields = ["created_by"]
    inlines = [LocationInline, ScheduleInline, BannerInline]

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
        return qs.filter(Q(created_by=request.user) | Q(status=EventStatus.ACTIVE))


@admin.register(EventSignup)
class EventSignupAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "event",
        "signup_date",
    )
    search_fields = (
        "user",
        "event",
        "signup_date",
    )
    list_filter = (
        "event",
        "signup_date",
    )
    readonly_fields = ["signup_date"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "address",
        "google_map_link",
    )
    search_fields = (
        "address",
        "google_map_link",
    )
    list_filter = ("address",)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "image",
    )
    search_fields = (
        "event",
        "image",
    )
    list_filter = ("event",)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "start_date",
        "start_time",
        "end_date",
        "end_time",
    )
    search_fields = (
        "event",
        "start_date",
        "start_time",
        "end_date",
        "end_time",
    )
    list_filter = (
        "event",
        "start_date",
        "start_time",
        "end_date",
        "end_time",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "is_active",
    )
    search_fields = (
        "name",
        "is_active",
    )
    list_filter = (
        "name",
        "is_active",
    )
    readonly_fields = [
        "created_at",
    ]
