# syntax=docker/dockerfile:1
FROM python:3.11.4-alpine AS builder
WORKDIR /app
EXPOSE 8080

COPY requirements.txt /app/
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore --upgrade --no-cache-dir --requirement requirements.txt --disable-pip-version-check
COPY ./app /app/
CMD ["python", "main.py"]