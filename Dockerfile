FROM python:3.12.4-slim

# Set environment variables
ENV APP_USER=event_user
ENV APP_GROUP=event_group
ENV APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create the user and group
RUN groupadd -r $APP_GROUP && \
    useradd -r -g $APP_GROUP -d $APP_HOME -s /sbin/nologin -c "Docker image user" $APP_USER

# Set the working directory
WORKDIR $APP_HOME

# Install minimal system dependencies and upgrade pip
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && pip install --no-cache-dir --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for caching
COPY requirements.txt requirements.txt
RUN pip install --no-compile -r requirements.txt

# Copy application code
COPY . .

# Fix permissions for installed packages
RUN chown -R $APP_USER:$APP_GROUP /usr/local/lib/python3.12/site-packages

# Set permissions for the application directory
RUN chown -R $APP_USER:$APP_GROUP $APP_HOME

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to the non-root user
USER $APP_USER

# Set the script as the container's entrypoint
ENTRYPOINT ["/entrypoint.sh"]
