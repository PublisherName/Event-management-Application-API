from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from root.env_config import env


class Command(BaseCommand):
    help = "Create an admin user if it does not exist"

    def handle(self, *args, **kwargs):
        admin_username = env("DJANGO_ADMIN_USERNAME")
        admin_password = env("DJANGO_ADMIN_PASSWORD")
        admin_email = env("DJANGO_ADMIN_EMAIL")

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(admin_username, admin_email, admin_password)
            self.stdout.write(self.style.SUCCESS(f'Admin user "{admin_username}" created'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin user "{admin_username}" already exists'))
