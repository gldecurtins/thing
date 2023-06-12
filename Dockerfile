# syntax=docker/dockerfile:1
FROM python:latest
WORKDIR /app
EXPOSE 8080
ARG REQUIREMENTS=requirements-dev.txt
COPY requirements.txt requirements-dev.txt /app/
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check
COPY . /app/
CMD ["python", "main.py"]