from django.http import JsonResponse
from rest_framework import status


def error404(request, exception):
    return JsonResponse(
        {"details": "Requested end point does not exist."}, status=status.HTTP_404_NOT_FOUND
    )


def error500(request):
    return JsonResponse(
        {"details": "Woooh! I'm Drunk."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
