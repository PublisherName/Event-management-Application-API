from django.contrib.auth.models import User
from django.db import models


class UserActivationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, default="", blank=True)
