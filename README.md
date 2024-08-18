# EVENT MANAGEMENT APPLICATION API
This is a simple event management application API that allows users to create, read, update, and delete events. The API is built using Django Rest Framework and utilizes Docker for containerization, RabbitMQ for message brokering, and Celery for task scheduling.

## Features
- Create an event
- Read all events
- Read a single event
- Update an event
- Delete an event

## Installation
1. Clone the repository
```bash
git clone git@github.com:PublisherName/Event-management-Application-API.git
```
2. Change directory to the project folder
```bash
cd Event-management-Application-API
```
3. run docker compose
```bash
DOPPLER_TOKEN="your_doppler_token" docker-compose up
```

## Doppler Configuration

1. Create a new project in Doppler

2. Create a new environment in the project

3. Import the following variables in the environment

```json
{
  "ALLOWED_HOSTS": "backend",
  "ALLOWED_ORIGINS": "http://backend:8000",
  "CELERY_BROKER_URL": "amqp://guest:guest@rabbitmq:5672//",
  "CELERY_RESULT_BACKEND": "django-db",
  "CSRF_COOKIE_SECURE": "False",
  "DEFAULT_FROM_EMAIL": "email@email.com",
  "DEVELOPMENT": "True",
  "DJANGO_SECRET_KEY": "YOUR_DJANGO_SECRET_KEY",
  "DOPPLER_TOKEN": "YOUR_DOPPLET_SERVICE_TOKEN",
  "EMAIL_HOST": "EMAIL.HOST",
  "EMAIL_HOST_PASSWORD": "EMAIL",
  "EMAIL_HOST_USER": "HOST_USER",
  "EMAIL_PORT": "2525",
  "EMAIL_USE_TLS": "True",
  "FRONTEND_URL": "http://frontend",
  "PROJECT_TITLE": "Event Management System",
  "SECURE_HSTS_INCLUDE_SUBDOMAINS": "True",
  "SECURE_HSTS_PRELOAD": "False",
  "SECURE_HSTS_SECONDS": "0",
  "SECURE_SSL_REDIRECT": "False",
  "SESSION_COOKIE_SECURE": "False"
}
```

4. Add the doppler service token to the docker-compose command while running the application

```bash
DOPPLER_TOKEN="your_doppler_token" docker-compose up
```
