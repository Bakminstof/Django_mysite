#!/usr/bin/env bash
docker-compose -f docker-compose.prod.yaml up --build -d

docker exec django_mysite python manage.py flush --no-input
docker exec django_mysite python manage.py migrate --noinput
docker exec django_mysite python manage.py init_discounts_taxes
docker exec django_mysite python manage.py create_random_items 10
docker exec django_mysite python manage.py collectstatic --no-input --clear

docker exec -ti django_mysite python manage.py createsuperuser
