# EVENT MANAGEMENT APPLICATION API
This is a simple event management application API that allows users to create, read, update and delete events. The API is built using Django Rest Framework.

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
3. Create a virtual environment
```bash
python3 -m venv venv
```
4. Activate the virtual environment
```bash
source venv/bin/activate
```
5. Install the project dependencies
```bash
pip install -r requirements.txt
```
6. Migration
```bash
python manage.py migrate
```
7. Run the application
```bash
python manage.py runserver
```

## RabbitMQ , Celery Installation

RabbitMQ and Celery are used in this project to handle asynchronous tasks and background job processing.

1. Install RabbitMQ
```bash
sudo pacman -S rabbitmq
```

2. Start RabbitMQ
```bash
sudo systemctl start rabbitmq
```

3. Enable RabbitMQ
```bash
sudo systemctl enable rabbitmq
```

4. Creating a user
```bash
sudo rabbitmqctl add_user djangouser 'randompassword*1'
```

5. Create a virtual host
```bash
sudo rabbitmqctl add_vhost event_management
```

6. Set permissions
```bash
sudo rabbitmqctl set_permissions -p event_management djangouser ".*" ".*" ".*"
```

7. Export the environment variables
```bash
export CELERY_BROKER_URL=amqp://djangouser:randompassword*1@localhost:5672/event_management
export CELERY_RESULT_BACKEND=rpc://
```

8. Run Celery
```bash
celery -A root worker --loglevel=info
```

## Gunicorn
Gunicorn is a WSGI HTTP server for UNIX. It is used to run the Django application in production.

1. Run Gunicorn
```bash
doppler run -- gunicorn --config gunicorn_config.py root.wsgi:application
```