import base64

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_rest_passwordreset.tokens import get_token_generator
from rest_framework import serializers

from auths.models import UserToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, allow_blank=False)
    confirm_password = serializers.CharField(write_only=True, allow_blank=False)
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    username = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirm_password",
        )

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise ValidationError("Passwords do not match.")
        if User.objects.filter(username=data["username"]).exists():
            raise ValidationError("Username already exists")
        if User.objects.filter(email=data["email"]).exists():
            raise ValidationError("Email already exists")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.is_active = False
        token = get_token_generator().generate_token(user)

        UserToken.objects.create(user=user, token=token).save()
        user.save()

        context = {
            "activation_link": settings.FRONTEND_URL
            + "/activate/"
            + base64.b64encode(validated_data["email"].encode("utf-8")).decode("utf-8")
            + "/"
            + base64.b64encode(token.encode("utf-8")).decode("utf-8"),
            "username": user.username,
            "token": token,
        }

        email_html_message = render_to_string("email/acc_active_email.html", context)
        email_plaintext_message = render_to_string("email/acc_active_email.txt", context)

        msg = EmailMultiAlternatives(
            "Account activation for {title}".format(title=settings.PROJECT_TITLE),
            email_plaintext_message,
            settings.DEFAULT_FROM_EMAIL,
            [validated_data["email"]],
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
        return user


class UserActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    token = serializers.CharField(required=True, allow_blank=False)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
            self.user_token = UserToken.objects.get(user=user, token=data["token"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")
        except UserToken.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")
        if user.is_active:
            raise serializers.ValidationError("User is already active.")
        return data

    def save(self):
        user = User.objects.get(email=self.validated_data["email"])
        user.is_active = True
        user.save()

    def delete(self):
        try:
            self.user_token.delete()
        except UserToken.DoesNotExist:
            raise serializers.ValidationError("Unable to clear user activation code.")


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ("username", "password")

    def validate(self, data):
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
            raise ValidationError("Must provide username and password both")
        return data


class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)
    confirm_password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ("password", "confirm_password", "old_password")

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise ValidationError("Passwords do not match.")
        if data["password"] == data["old_password"]:
            raise ValidationError("New password cannot be same as old password.")
        return data

    def update(self, instance, validated_data):
        if not self.instance.check_password(validated_data["old_password"]):
            raise ValidationError("Old password is incorrect.")
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
