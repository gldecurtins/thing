FROM python:3.11.4-alpine
WORKDIR /app

COPY ./app /app
RUN pip install --upgrade pip
RUN pip install --upgrade --no-cache-dir --requirement requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]