from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"

    def ready(self):  # noqa: PLR6301
        import events.signals  # type: ignore # noqa: F401
        import events.validators  # type: ignore # noqa: F401
