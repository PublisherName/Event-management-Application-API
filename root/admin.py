from django.contrib import admin
from django_celery_results.models import TaskResult


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ("task_id", "status", "date_done", "task_name", "worker", "result")
    search_fields = ("task_id", "status", "task_name", "worker")
    readonly_fields = (
        "task_id",
        "status",
        "date_done",
        "task_name",
        "worker",
        "result",
        "traceback",
        "meta",
    )
    list_filter = ("status", "date_done", "task_name", "worker")
    date_hierarchy = "date_done"
