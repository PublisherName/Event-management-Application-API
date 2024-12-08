from datetime import datetime, timedelta
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from faker import Faker
from PIL import Image

from events.enums.status import EventStatus
from events.models.banner import Banner
from events.models.category import Category
from events.models.event import Event
from events.models.location import Location
from events.models.schedule import Schedule
from root.env_config import env

fake = Faker()


class Command(BaseCommand):
    help = "Populate the Event model with fake data"

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(
            username=env("FAKER_USERNAME"), defaults={"password": env("FAKER_PASSWORD")}
        )

        for _ in range(4):
            self.create_category()

        for _ in range(10):
            description_html = "".join(fake.paragraphs(nb=3, ext_word_list=None))
            event = Event.objects.create(
                title=fake.sentence(nb_words=6),
                description=f"<p>{description_html}</p>",
                category=Category.objects.filter(is_active=True).order_by("?").first(),
                total_participants=fake.random_int(min=10, max=100),
                created_by=user,
                status=EventStatus.DRAFT,
            )

            self.create_location(event)
            self.create_schedule(event)
            self.create_banner(event)

            event.status = fake.random_element(elements=[status.name for status in EventStatus])
            event.save()

            self.stdout.write(self.style.SUCCESS(f"Successfully created event: {event.title}"))

    @staticmethod
    def create_image():
        image = Image.new("RGB", (100, 100), color="blue")
        image_io = BytesIO()
        image.save(image_io, format="PNG")
        image_io.seek(0)

        image_name = fake.uuid4() + ".png"
        return ContentFile(image_io.read(), image_name)

    @staticmethod
    def create_schedule(event):
        today = datetime.today().date()
        start_date = today + timedelta(days=fake.random_int(min=1, max=30))
        end_date = start_date + timedelta(days=fake.random_int(min=1, max=30))
        start_time = fake.date_time().time().strftime("%H:%M:%S")
        start_time_full = datetime.combine(
            start_date, datetime.strptime(start_time, "%H:%M:%S").time()
        )
        end_time_full = start_time_full + timedelta(hours=5)
        end_time = end_time_full.time().strftime("%H:%M:%S")

        return Schedule.objects.create(
            event=event,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
        )

    def create_banner(self, event):
        Banner.objects.create(
            event=event,
            image=self.create_image(),
            uploaded_at=fake.date_time_this_year(),
        )

    @staticmethod
    def create_location(event):
        Location.objects.create(
            event=event,
            address=fake.address(),
            google_map_link=fake.url(),
        )

    def create_category(self):
        return Category.objects.create(
            name=fake.word(),
            description=fake.sentence(),
            icon=self.create_image(),
            is_active=fake.boolean(chance_of_getting_true=50),
        )
