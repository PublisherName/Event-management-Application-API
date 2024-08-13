from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from auths.models import UserToken


def validate_user_registration(data):
    if data["password"] != data["confirm_password"]:
        raise ValidationError("Passwords do not match.")
    if User.objects.filter(username=data["username"]).exists():
        raise ValidationError("Username already exists")
    if User.objects.filter(email=data["email"]).exists():
        raise ValidationError("Email already exists")
    return data


def validate_user_activation(data):
    try:
        user = User.objects.get(email=data["email"])
        user_token = UserToken.objects.get(user=user, token=data["token"])
    except User.DoesNotExist:
        raise ValidationError("Invalid credentials.")
    except UserToken.DoesNotExist:
        raise ValidationError("Invalid credentials.")
    if user.is_active:
        raise ValidationError("User is already active.")
    return data, user_token


def validate_user_token_delete(user_token):
    try:
        user_token.delete()
    except UserToken.DoesNotExist:
        raise ValidationError("Unable to clear user activation code.")


def validate_user_login(data):
    username = data["username"]
    password = data["password"]

    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                data["user"] = user
            else:
                raise ValidationError("User is not active")
        else:
            raise ValidationError("Invalid username or password")
    else:
        raise ValidationError("Must provide username and password both")
    return data


def validate_user_change_password(data):
    if data["password"] != data["confirm_password"]:
        raise ValidationError("Passwords do not match.")
    if data["password"] == data["old_password"]:
        raise ValidationError("New password cannot be same as old password.")
    return data


def validate_old_password(instance, old_password):
    if not instance.check_password(old_password):
        raise ValidationError("Old password is incorrect.")
