import json
from pathlib import Path

from django.core.management.base import BaseCommand

from preferences.models import EmailTemplate


class Command(BaseCommand):
    help = "Seed the database with preferences data from preferences.json"

    def handle(self, *args, **kwargs):
        file_path = (
            Path(__file__).resolve().parent.parent.parent.parent / "seeds" / "preferences.json"
        )
        with open(file_path) as file:
            data = json.load(file)
            for item in data:
                model = item["model"]
                if model == "preferences.emailtemplate":
                    fields = item["fields"]
                    EmailTemplate.objects.update_or_create(pk=item["pk"], defaults=fields)
        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
