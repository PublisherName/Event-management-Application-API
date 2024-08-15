import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")

app = Celery("root")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.update(
    broker_url=os.getenv("CELERY_BROKER_URL"),
    result_backend=os.getenv("CELERY_RESULT_BACKEND"),
    broker_connection_retry_on_startup=True,
    email_task_config={"ignore_result": False},
    email_chunk_size=1,
    task_serializer="json",
    result_serializer="json",
    result_extended=True,
    timezone="Asia/Kathmandu",
    enable_utc=True,
)
