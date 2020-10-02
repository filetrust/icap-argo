# Specify BROKER_URL and QUEUE when running
FROM python:3.8-slim
WORKDIR /app
COPY . .
ENTRYPOINT ["python", "-m", "message_reader_app"]