from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ["created_by"]

    def save(self, **kwargs):
        user = self.context["request"].user
        if not user.is_superuser:
            self.validated_data["is_verified"] = False
        try:
            return super().save(**kwargs)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)

    @staticmethod
    def delete(instance, request):
        if not (request.user == instance.created_by or request.user.is_superuser):
            raise PermissionDenied("You do not have permission to delete this event.")
        instance.delete()

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if not (request.user == instance.created_by or request.user.is_superuser):
            raise PermissionDenied("You do not have permission to update this event.")
        return super().update(instance, validated_data)
