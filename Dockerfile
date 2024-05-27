FROM python:3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=config.settings

RUN apt-get update -qq && apt-get install -y libpq-dev
