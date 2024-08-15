from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import authentication, serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auths.serializers import (
    UserActivationSerializer,
    UserChangePasswordSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


class UserRegistrationViewSet(viewsets.ViewSet):
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(request_body=UserRegistrationSerializer, tags=["User Management"])
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            if user:
                return Response(
                    {"status": "User created. Please verify email to activate account."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivationViewSet(viewsets.ViewSet):
    serializer_class = UserActivationSerializer

    @swagger_auto_schema(request_body=UserActivationSerializer, tags=["User Management"])
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.delete()
            return Response({"status": "User activated."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(viewsets.ViewSet):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(request_body=UserLoginSerializer, tags=["User Management"])
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        token_user = self.request.auth.user if self.request.auth else None
        if user != token_user:
            return User.objects.none()
        return User.objects.filter(pk=self.request.user.pk)

    @swagger_auto_schema(tags=["User Management"])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=["User Management"])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserChangePasswordViewSet(viewsets.ViewSet):
    serializer_class = UserChangePasswordSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UserChangePasswordSerializer, tags=["User Management"])
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.update(request.user, serializer.validated_data)
            return Response({"status": "Password changed"}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
