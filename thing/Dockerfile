FROM python:3.11.4-alpine
WORKDIR /app
ARG REQUIREMENTS=requirements.txt

COPY ./app /app
RUN pip install --upgrade pip
RUN pip install --upgrade --no-cache-dir --requirement $REQUIREMENTS

EXPOSE 8000
CMD ["python", "main.py"]