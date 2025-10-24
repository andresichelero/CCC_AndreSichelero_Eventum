FROM python:3.10-slim
WORKDIR /app
# used to check if Postgres is ready and for virus scanning
RUN apt-get update && apt-get install -y netcat-openbsd clamav clamav-daemon libmagic1 libmagic-dev
RUN freshclam
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
