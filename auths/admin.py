import contextlib

from django.contrib import admin
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework.authtoken.models import TokenProxy

with contextlib.suppress(admin.sites.NotRegistered):
    admin.site.unregister(TokenProxy)

with contextlib.suppress(admin.sites.NotRegistered):
    admin.site.unregister(ResetPasswordToken)
