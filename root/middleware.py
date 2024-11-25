import os
import uuid


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
