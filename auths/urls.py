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

from django.urls import include, path
from django_rest_passwordreset.views import (
    ResetPasswordConfirmViewSet,
    ResetPasswordRequestTokenViewSet,
    ResetPasswordValidateTokenViewSet,
)
from rest_framework import routers

from auths.views import (
    UserActivationViewSet,
    UserChangePasswordViewSet,
    UserDetailsViewSet,
    UserLoginViewSet,
    UserRegistrationViewSet,
)

router = routers.DefaultRouter()

router.register(r"register", UserRegistrationViewSet, basename="register")

router.register(r"activate", UserActivationViewSet, basename="activate")

router.register(r"login", UserLoginViewSet, basename="login")

router.register(r"forgot-password", ResetPasswordRequestTokenViewSet, basename="forgot-password")

router.register(
    r"validate-password-reset-token", ResetPasswordValidateTokenViewSet, basename="validate-token"
)

router.register(r"reset-password", ResetPasswordConfirmViewSet, basename="reset-password")

router.register(r"profile", UserDetailsViewSet, basename="profile")

router.register(r"change-password", UserChangePasswordViewSet, basename="change-password")

urlpatterns = [
    path("", include(router.urls)),
]
