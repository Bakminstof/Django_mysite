#!/usr/bin/env bash
## Run development server without docker on `127.0.0.5:7777`
docker-compose -f docker-compose.dev.yaml up --build -d postgres_django  # Start Postgres container on `0.0.0.0:4343`
#python -m pip install environs
export DEVELOPMENT=1 SQL_DB_HOST=0.0.0.0 && python django_site/mysite/manage.py runserver 127.0.0.5:7777

## Run development server with docker on `127.0.0.5:7777`
#export DOCKER=1 && docker-compose -f docker-compose.dev.yaml up --build -d
