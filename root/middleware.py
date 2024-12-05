import os
import uuid

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class FileRenameMiddleware:
    """
    Middleware to rename uploaded files before they are processed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ["POST", "PUT", "PATCH"] and request.FILES:
            for _, file_obj in request.FILES.items():
                ext = os.path.splitext(file_obj.name)[1]
                file_obj.name = f"{uuid.uuid4().hex}{ext}"
        return self.get_response(request)


class HandlePermissionDeniedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):  # noqa: PLR6301 # skipcq: PYL-R0201
        if isinstance(exception, PermissionDenied):
            messages.error(request, str(exception))
            return redirect(request.headers.get("referer", "/"))
        return None
