from django.contrib.auth.models import User
from django.db import models


class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500, null=True, blank=True)
