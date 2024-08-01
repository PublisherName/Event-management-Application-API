from django.http import JsonResponse
from rest_framework import status


def error404(request, exception):
    return JsonResponse(
        {
            "details": "Requested end point does not exist.",
            "requested_url": request.path,
            "error": type(exception).__name__,
        },
        status=status.HTTP_404_NOT_FOUND,
    )


def error500(request):
    return JsonResponse(
        {
            "details": "Woooh! I'm Drunk.",
            "requested_url": request.path,
            "error": "Server Error",
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
