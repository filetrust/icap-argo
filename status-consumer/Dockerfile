# Specify BROKER_URL and QUEUE when running
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install pika
ENTRYPOINT ["python", "-m", "status_consumer_app"]