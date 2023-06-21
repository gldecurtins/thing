# syntax=docker/dockerfile:1
FROM python:3.11.4-alpine AS aiohttp
ARG REQUIREMENTS=requirements-dev.txt
WORKDIR /app
COPY requirements.txt requirements-dev.txt /app/
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check
COPY . /app/