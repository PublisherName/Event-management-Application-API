"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import (
    handler404,
    handler500,
)
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from auths.urls import router as auths_urlpatterns
from events.urls import router as events_urlpatterns
from root.views import health_check

router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Event Management API",
        default_version="v1",
        description="API for managing events",
        contact=openapi.Contact(email="event@subashghimire.info.np"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router.registry.extend(auths_urlpatterns.registry)
router.registry.extend(events_urlpatterns.registry)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include(router.urls)),
        path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        path("health/", health_check, name="health-check"),
        path("summernote/", include("django_summernote.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

handler404 = "root.views.error404"  # noqa: F811
handler500 = "root.views.error500"  # noqa: F811
