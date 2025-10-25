FROM python:3.10-alpine

WORKDIR /app
# used to check if Postgres is ready
RUN apk add --no-cache netcat-openbsd libmagic
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
