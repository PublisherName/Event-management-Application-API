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

3. Copy the .env.example file to .env
```bash
cp .env.example .env
```

4. run docker compose
```bash
docker-compose up --build
```