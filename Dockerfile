FROM python:3.12.4-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y curl wget gnupg

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip -r requirements.txt
