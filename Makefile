create_django_user_function:
	@echo "Creating Django superuser..."
	@if python manage.py shell -c "exit(0 if __import__('django.contrib.auth').contrib.auth.get_user_model().objects.filter(username='$${DJANGO_SUPERUSER_USERNAME:-admin}').exists() else 1)"; then \
		echo "Superuser already exists."; \
	else \
		DJANGO_SUPERUSER_USERNAME=$${DJANGO_SUPERUSER_USERNAME:-admin} \
		DJANGO_SUPERUSER_EMAIL=$${DJANGO_SUPERUSER_EMAIL:-test@test.com} \
		DJANGO_SUPERUSER_PASSWORD=$${DJANGO_SUPERUSER_PASSWORD:-admin} \
		python manage.py createsuperuser --noinput && \
		echo "Superuser $${DJANGO_SUPERUSER_USERNAME} created successfully" || \
		echo "Error: Superuser creation failed. Please check environment variables."; \
	fi

check_django_user_env:
	@if [ "$${ENV:-development}" = "production" ]; then \
		if [ -z "$${DJANGO_SUPERUSER_USERNAME}" ] || [ -z "$${DJANGO_SUPERUSER_EMAIL}" ] || [ -z "$${DJANGO_SUPERUSER_PASSWORD}" ]; then \
			echo "Error: All superuser credentials must be explicitly set in production" && exit 1; \
		fi \
	fi
	@if [ -z "$${DJANGO_SUPERUSER_USERNAME}" ]; then \
		echo "Warning: DJANGO_SUPERUSER_USERNAME not set. Defaulting to 'admin'"; \
	fi
	@if [ -z "$${DJANGO_SUPERUSER_EMAIL}" ]; then \
		echo "Warning: DJANGO_SUPERUSER_EMAIL not set. Defaulting to 'test@test.com'"; \
	fi
	@if [ -z "$${DJANGO_SUPERUSER_PASSWORD}" ]; then \
		echo "Warning: DJANGO_SUPERUSER_PASSWORD not set. Defaulting to 'admin'"; \
	fi

create_django_user: check_django_user_env create_django_user_function

django_migrate:
	python manage.py makemigrations || (echo "Error: Failed to make migrations" && exit 1)
	python manage.py migrate || (echo "Error: Failed to apply migrations" && exit 1)
	python manage.py collectstatic --noinput || (echo "Error: Failed to collect static files" && exit 1)

gunicorn_serve:
	gunicorn -b $${GUNICORN_BIND:-0.0.0.0:8000} \
		--worker-class=$${GUNICORN_WORKER_CLASS:-gevent} \
		--worker-connections=$${GUNICORN_WORKER_CONNECTIONS:-1000} \
		--workers=$${GUNICORN_WORKERS:-2} \
		root.wsgi

django_serve: django_migrate gunicorn_serve

create_rabbitmq_user:
	sudo rabbitmqctl add_user $${RABBITMQ_USER:-defaultUser} $${RABBITMQ_PASSWORD:-defaultPassword}
	sudo rabbitmqctl set_user_tags $${RABBITMQ_USER:-defaultUser} administrator
	sudo rabbitmqctl add_vhost $${RABBITMQ_VHOST:-defaultVhost}
	sudo rabbitmqctl set_permissions -p $${RABBITMQ_VHOST:-defaultVhost} $${RABBITMQ_USER:-defaultUser} ".*" ".*" ".*"

worker_run:
	celery -A root worker \
		--loglevel=$${CELERY_LOG_LEVEL:-info} \
		--logfile=$${LOG_DIR:-logs}/celery.log \
		--logfile-backups=$${CELERY_LOG_BACKUPS:-10} \
		-s $${CELERY_SCHEDULE_FILE:-/tmp/celerybeat-schedule} \
		--concurrency=$${CELERY_CONCURRENCY:-4} \
		-Q $${CELERY_QUEUE:-default} \
		--max-tasks-per-child=$${CELERY_MAX_TASKS_PER_CHILD:-100}

worker_ping:
	celery -A root inspect ping || (echo "Error: Worker not responding" && exit 1)
