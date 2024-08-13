from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from auths.validators import (
    validate_old_password,
    validate_user_activation,
    validate_user_change_password,
    validate_user_login,
    validate_user_registration,
    validate_user_token_delete,
)


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

    @staticmethod
    def validate(data):
        return validate_user_registration(data)

    @staticmethod
    def create(validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()
        return user


class UserActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    token = serializers.CharField(required=True, allow_blank=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_token = None

    def validate(self, data):
        data, self.user_token = validate_user_activation(data)
        return data

    @staticmethod
    def create(validated_data):
        user = User.objects.get(email=validated_data["email"])
        user.is_active = True
        user.save()
        return user

    @staticmethod
    def update(instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.email = validated_data.get("email", instance.email)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance

    def delete(self):
        validate_user_token_delete(self.user_token)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ("username", "password")

    @staticmethod
    def validate(data):
        return validate_user_login(data)

    @staticmethod
    def create(validated_data):
        user = validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return {"token": token.key}


class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)
    confirm_password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ("password", "confirm_password", "old_password")

    @staticmethod
    def validate(data):
        validate_user_change_password(data)
        return data

    @staticmethod
    def update(instance, validated_data):
        validate_old_password(instance, validated_data["old_password"])
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
