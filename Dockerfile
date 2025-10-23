FROM python:3.10-slim
WORKDIR /app
# used to check if Postgres is ready
RUN apt-get update && apt-get install -y netcat-openbsd 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
