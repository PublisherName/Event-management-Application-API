from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventSignupViewSet, EventViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet)
router.register(r"eventsignups", EventSignupViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
