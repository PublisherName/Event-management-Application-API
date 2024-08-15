FROM python:3.12.4-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y curl wget gnupg

# Install Doppler CLI
RUN (curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh || wget -t 3 -qO- https://cli.doppler.com/install.sh) | sh

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip -r requirements.txt