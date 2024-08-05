from django.apps import AppConfig


class AuthsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auths"

    def ready(self):  # noqa: PLR6301
        import auths.signals  # type: ignore # noqa: F401
